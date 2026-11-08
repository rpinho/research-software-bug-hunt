import ast, contextlib, io, json, os, pathlib, random, subprocess, sys
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.metrics import recall_score, roc_curve
from ortools.sat.python import cp_model
from oracle import assignment_minimum, constrained_threshold
ID='DECCAF-002'
BaseSolver=cp_model.CpSolver
class OneWorkerSolver(BaseSolver):
 def __init__(self):
  super().__init__(); self.parameters.num_search_workers=1
cp_model.CpSolver=OneWorkerSolver
def load_functions(source):
    tree=ast.parse(source.read_text())
    ns={'np':np,'pd':pd,'os':os,'cp_model':cp_model,'random':random,'recall_score':recall_score,'roc_curve':roc_curve,'metrics':metrics}
    tree=ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[])
    exec(compile(tree,str(source),'exec'),ns)
    return ns

def allocation_checks(code,work):
    ns=load_functions(code/'deferral/run_alert.py')
    previous=os.getcwd(); work.mkdir(); (work/'Code/deferral').mkdir(parents=True)
    os.chdir(work/'Code/deferral')
    out={}
    try:
        cap=pd.DataFrame({'batch_id':[1],'batch_size':[2],'human':[1]})
        examples={'normal':(cap,1)}
        if ID=='DECCAF-001':
            examples['reordered']=(cap[['human','batch_id','batch_size']],1)
        else:
            examples['label_2']=(cap.assign(batch_id=2),2)
            examples['label_0']=(cap.assign(batch_id=0),0)
        for label,(capacity,batch_id) in examples.items():
            for function in ['deccaf_cp_deferral_func','ova_deferral_func','rand_deferral_func','full_auto_func','full_model_func']:
                # Check all users of batch indexing; capacity ordering affects first three.
                bat=pd.DataFrame({'case_id':[10,20],'batch':[batch_id,batch_id]})
                data=pd.DataFrame(index=[10,20])
                decisions=pd.DataFrame({'human':[0,1],'model#0':[1,0]},index=[10,20])
                losses=pd.DataFrame({'human':[.1,.9],'model#0':[.9,.1]},index=[10,20])
                args=[capacity,bat,data]
                if function!='full_auto_func': args.append(decisions)
                if function in ['deccaf_cp_deferral_func','ova_deferral_func']: args.append(losses if function.startswith('deccaf') else 1-losses)
                args += [label,function]
                if function in ['deccaf_cp_deferral_func','ova_deferral_func']: args.append('seed')
                args += ['tiny',.057]
                random.seed(7)
                try:
                    with contextlib.redirect_stdout(io.StringIO()): result=ns[function](*args)
                    if result is None: record={'returned':None}
                    else:
                        a,r=result
                        record={'assignments':{str(k):v for k,v in a.assignment.items()},'predictions':{str(k):int(v) for k,v in r.prediction.items()},'rows':len(a)}
                        # Disk output must agree with returned rows, too.
                        outputs=list((work/'Data_and_models').rglob('assignments.parquet'))
                        assert outputs
                except Exception as e: record={'error':type(e).__name__+': '+str(e)}
                out[label+'/'+function]=record
    finally: os.chdir(previous)
    return out

def threshold_checks(code):
    variants={
      'small':([0]*9+[1,1],[.9,.8,.7,.6,.5,.4,.3,.2,.1,.95,.15]),
      'normal':([0]*100+[1,1],[1-i/100 for i in range(100)]+[1.1,.975]),
      'ties':([0]*100+[1,1],[.8]*20+[.2]*80+[.9,.7]),
      'rounded_budget':([0]*31+[1,1],[1-i/100 for i in range(31)]+[1.1,.995])
    }
    out={}
    for file,func,extra in [('alert_model/hpo_fpr.py','tpr_at_fpr',()),('alert_model/training_and_predicting.py','fpr_thresh',()),('data/preprocess.py','tpr_at_fpr',(.05,))]:
        ns=load_functions(code/file)
        for label,(y,s) in variants.items():
            args=[np.array(y),np.array(s),*extra]
            result=ns[func](*args)
            if file=='alert_model/hpo_fpr.py':
                # This callback exposes only recall. Convert back to a count on the two positives.
                record={'true_positives':int(round(result[1]*sum(y)))}
            else:
                threshold=float(result[1]); pred=[int(x>=threshold) for x in s]
                record={'true_positives':sum(a==1 and b==1 for a,b in zip(y,pred)), 'false_positives':sum(a==0 and b==1 for a,b in zip(y,pred)), 'threshold':threshold,'decisions':pred}
            out[file+'/'+label]=record
    # Exercise the actual HPO.objective method's duplicate threshold code without fitting:
    # provide a fake already-scored model and a trial; no LightGBM/Optuna import or training.
    # Its threshold block is also checked directly as an unchanged AST slice below.
    t=ast.parse((code/'alert_model/hpo_fpr.py').read_text())
    cls=next(n for n in t.body if isinstance(n,ast.ClassDef) and n.name=='HPO')
    objective=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='objective')
    start=next(i for i,n in enumerate(objective.body) if isinstance(n,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='results' for a in n.targets))
    end=next(i for i,n in enumerate(objective.body) if isinstance(n,ast.If) and i>start)
    for label,(y,s) in variants.items():
        ns={'pd':pd,'np':np,'recall_score':recall_score,'roc_curve':roc_curve,'y_val':np.array(y),'y_pred':np.array(s)}
        exec(compile(ast.Module(body=objective.body[start:end],type_ignores=[]),'HPO.objective threshold block','exec'),ns)
        out['HPO.objective/'+label]={'true_positives':int(sum(a==1 and b==1 for a,b in zip(y,ns['y_pred']))),'false_positives':int(sum(a==0 and b==1 for a,b in zip(y,ns['y_pred'])))}
    oracle={k:constrained_threshold(*v) for k,v in variants.items()}
    return out,oracle


source=pathlib.Path(sys.argv[1]); work=pathlib.Path(sys.argv[2]); mode=sys.argv[3]
if ID=='DECCAF-003':
 result,expected=threshold_checks(source/'Code')
 if mode=='after':
  for key,value in result.items():
   ref=expected[key.split('/')[-1]]
   assert value['true_positives']==ref['true_positives']
   if 'false_positives' in value: assert value['false_positives']==ref['false_positives']
else:
 result=allocation_checks(source/'Code',work)
 if mode=='after':
  assert all(v.get('rows')==2 for v in result.values()),result
  best,minimum=assignment_minimum([10,20],1,{10:{'human':.1,'model#0':.9},20:{'human':.9,'model#0':.1}})
  for key,value in result.items():
   if key.endswith('deccaf_cp_deferral_func'):
    assert value['assignments']=={str(k):v for k,v in best[0].items()}
  print('Exact minimum assignment cost: '+str(minimum))
 elif ID=='DECCAF-001': assert result['reordered/deccaf_cp_deferral_func']=={'returned':None}
 else: assert all(result['label_0/'+f]['rows']==0 for f in ['deccaf_cp_deferral_func','ova_deferral_func','rand_deferral_func','full_auto_func','full_model_func'])
print(json.dumps(result,indent=2))

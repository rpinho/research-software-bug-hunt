args <- commandArgs(TRUE)
.libPaths(c(args[1], Sys.getenv('R_LIBS_USER'), .libPaths()))
suppressPackageStartupMessages(library(funscoR))
options(mc.cores=1)
# Synthetic numeric rows only; no biological data, scoring, or prediction.
n <- 120
acc <- sprintf('toy%03d',1:n)
features <- data.frame(residue=rep('S',n),x=(1:n)/n,z=sin(1:n),row.names=paste(acc,1,sep='_'))
gold <- data.frame(acc=acc[seq(2,n,2)],position=1)
parameters <- list(outfoldtimes=1,outfoldk=3,alogrithm='gbm',n_trees=2,interaction.depth=1,shrinkage=.1,n_minobsinnode=2)
custom <- tryCatch(train_funscore(features,'ST',gold,parameters=parameters,seed=11,ncores=1),error=function(e)e)
if(inherits(custom,'error')) {
 cat('CUSTOM ERROR:',conditionMessage(custom),'\n')
 custom_ok <- 0; custom_repeats <- 0; custom_trees <- 0
} else {
 custom_ok <- 1
 custom_repeats <- length(custom$models)
 custom_trees <- custom$models[[1]][[1]]$bestTune$n.trees
 stopifnot(identical(custom$variables$parameters,parameters),custom_repeats==1,length(custom$models[[1]])==3,custom_trees==2)
 cat('CUSTOM OK: 1 repetition, 3 folds, 2 trees each\n')
}
normal <- train_funscore(features,'ST',gold,seed=11,ncores=1)
# Compare the actual fitted numeric functions too, without making predictions.
weights <- unlist(lapply(normal$models,function(iter)lapply(iter,function(m)m$finalModel$initF)))
values <- c(custom_ok=custom_ok,custom_repeats=custom_repeats,custom_trees=custom_trees,normal_repeats=length(normal$models),normal_folds=length(normal$models[[1]]),normal_trees=normal$models[[1]][[1]]$bestTune$n.trees,normal_init_sum=sum(weights))
# Save complete trees and folds, omitting elapsed times and caller environments.
normal_parts <- lapply(normal$models,function(iter)lapply(iter,function(m)list(trees=m$finalModel$trees,initF=m$finalModel$initF,bestTune=m$bestTune)))
saveRDS(list(folds=normal$folds,parts=normal_parts),paste0(args[2],'.normal.rds'),version=2,compress=FALSE)
write.table(data.frame(metric=names(values),value=as.numeric(values)),args[2],sep='\t',quote=FALSE,row.names=FALSE)
print(values)

args <- commandArgs(TRUE);repo <- args[1];mode <- args[2]
here <- dirname(sub('^--file=', '', grep('^--file=', commandArgs(), value=TRUE)))
suppressPackageStartupMessages({library(data.table);library(RColorBrewer)})
setDTthreads(1)
e <- new.env();sys.source(file.path(repo,'R/core_mimosa2_funcs.R'),envir=e)
x <- fread(file.path(here,'contributions.csv'))
# A missing species/sample row means zero, as in the function's default matrix path.
for (cov in c(FALSE,TRUE)) {
 out <- e$calculate_var_shares_linear(copy(x),model_cov=cov)
 setorder(out,Species)
 fwrite(out,file.path(here,paste0(mode,if(cov) '-cov.csv' else '-matrix.csv')))
 cat(if(cov) 'model_cov=TRUE' else 'model_cov=FALSE',': ',paste(paste(out$Species,out$VarShare,sep='='),collapse=', '),'\n',sep='')
 if(mode=='after' || !cov) stopifnot(isTRUE(all.equal(out$VarShare,c(0,1,0))))
 else stopifnot(identical(out$VarShare,c(0,0,0)))
}
# Normal input: same table with the zero row explicitly present.
dense <- rbind(copy(x),data.table(compound='M',Species='B',Sample='s2',newValue=0))
setorder(dense,Species,Sample)
normal <- as.data.frame(e$calculate_var_shares_linear(copy(dense),model_cov=TRUE))
if(mode=='before') {saveRDS(normal,file.path(here,'.normal-before.rds'))} else {
 stopifnot(identical(normal,readRDS(file.path(here,'.normal-before.rds'))))
 cat('Dense normal input: exactly unchanged.\n')
}

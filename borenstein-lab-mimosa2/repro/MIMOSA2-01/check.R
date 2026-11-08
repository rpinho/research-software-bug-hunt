args <- commandArgs(TRUE);repo <- args[1]; mode <- args[2]
here <- dirname(sub('^--file=', '', grep('^--file=', commandArgs(), value=TRUE)))
suppressPackageStartupMessages({library(data.table);library(RColorBrewer)})
setDTthreads(1)
e <- new.env();sys.source(file.path(repo,'R/core_mimosa2_funcs.R'),envir=e)
kos <- fread(file.path(here,'kos.csv'));network <- fread(file.path(here,'network.csv'))
results <- list()
for(normalize in c(TRUE,FALSE)) for(rel in c(TRUE,FALSE)) for(remove_rev in c(TRUE,FALSE)){
  out <- e$get_species_cmp_scores(copy(kos),copy(network),kos_only=TRUE,normalize=normalize,relAbund=rel,remove_rev=remove_rev)
  direct <- e$get_cmp_scores_kos(copy(kos),copy(network),normalize=normalize,relAbund=rel,remove_rev=remove_rev)
  same <- isTRUE(all.equal(out,direct))
  if(mode=='after') stopifnot(same)
  if(rel && remove_rev) stopifnot(same)
  out[,`:=`(normalize=normalize,relAbund=rel,remove_rev=remove_rev)]
  results[[length(results)+1L]] <- out
  cat('normalize=',normalize,' relAbund=',rel,' remove_rev=',remove_rev,': ',paste(paste(out$compound,out$CMP,sep='='),collapse=', '),' (matches direct call: ',same,')\n',sep='')
}
out <- rbindlist(results)
fwrite(out,file.path(here,paste0(mode,'.csv')))
normal <- as.data.frame(out[relAbund==TRUE & remove_rev==TRUE])
if(mode=='before') {saveRDS(normal,file.path(here,'.normal-before.rds'))} else {stopifnot(identical(normal,readRDS(file.path(here,'.normal-before.rds'))));cat('Normal/default KO path: unchanged for both normalize settings.\n')}

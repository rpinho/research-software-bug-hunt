args <- commandArgs(TRUE)
repo <- args[1]; mode <- args[2]
here <- dirname(sub('^--file=', '', grep('^--file=', commandArgs(), value=TRUE)))
suppressPackageStartupMessages({library(igraph);library(dplyr);library(logger)})
log_threshold(ERROR)
e <- new.env(); sys.source(file.path(repo,'R/utils.R'),envir=e)
edges <- read.csv(file.path(here,'edges.csv'))
nodes <- read.csv(file.path(here,'nodes.csv'))
normal <- NULL
for (coverage in c('partial','metabolites_complete','ECs_complete','both_complete')) {
 ec <- subset(nodes, type=='EC',select=c(feature,pval,anchor))
 mt <- subset(nodes, type=='Metabolite',select=c(feature,pval,anchor))
 if (!coverage %in% c('ECs_complete','both_complete')) ec <- ec[1,,drop=FALSE]
 if (!coverage %in% c('metabolites_complete','both_complete')) mt <- mt[1,,drop=FALSE]
 result <- tryCatch(e$init_graph(edges, mt, ec),error=function(x) x)
 if (inherits(result,'error')) {
   cat(coverage, ': ERROR: ', conditionMessage(result),'\n',sep='')
   stopifnot(mode %in% c('before','release'),coverage!='partial')
 } else {
   v <- igraph::as_data_frame(result,what='vertices')
   v <- v[order(v$name),c('name','pval','anchor','type','imputed')]
   write.csv(v,file.path(here,paste(mode,coverage,'vertices.csv',sep='-')),row.names=FALSE,na='NA')
   ed <- igraph::as_data_frame(result,what='edges'); ed <- ed[order(ed$from,ed$to),]
   edge_keys <- function(x) sort(apply(x[,c('from','to')],1,function(pair) paste(sort(pair),collapse='|')))
   stopifnot(identical(unname(edge_keys(ed)),unname(edge_keys(edges))),vcount(result)==4L,ecount(result)==2L)
   write.csv(ed,file.path(here,paste(mode,coverage,'edges.csv',sep='-')),row.names=FALSE)
   cat(coverage, ': ',vcount(result),' vertices, ',ecount(result),' edges, ',sum(v$imputed),' imputed nodes\n',sep='')
   if (coverage=='partial') {
     if (mode=='before') saveRDS(list(v,ed),file.path(here,'.normal-before.rds'))
     else stopifnot(identical(list(v,ed),readRDS(file.path(here,'.normal-before.rds'))))
   }
 }
}
if(mode=='after') cat('Normal partial-coverage graph and all attributes: unchanged.\n')

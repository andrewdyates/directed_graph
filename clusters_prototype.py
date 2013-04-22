from __future__ import division
from __init__ import *
import matrix_io as mio
from clusters_prototype_lib import *

min_d=0.30
cls_fname="data/D.expr.gold.CLS.apr.19.tab"
dcor_fname="data/D.expr.gold.DCOR.apr.19.tab"
color_fname="data/gold.celegans.phase.colors.genes.txt"
graphviz_cmd="dot"
weak_fname="data/gold.weak.tab"
outpath_prefix="~/Desktop/gold_0.30_cluster_proto"
clusts_fname="data/gold.k7.hclust.csv"

CLS_D = mio.load(cls_fname)
DCOR_D = mio.load(dcor_fname)
WEAK_D = mio.load(weak_fname)
CLS = CLS_D['M']
DCOR = DCOR_D['M']
WEAK = WEAK_D['M']
names = CLS_D['row_ids']
CLUSTS = load_clusters(open(clusts_fname))

# Convert cluster names into row IDs (indexed from zero)
C = clust_names_to_row_nums(CLUSTS, names)

# break CLS, DCOR, and WEAK into inter-intra clusters
# collapse CLS, DCOR, and WEAK into composite cluster matrices, then plot
# for each cluster, extract each, then plot

clust_names = sorted(C.keys())
n = len(clust_names)
CLS_C = np.zeros((n,n))
DCOR_C = np.zeros((n,n))
WEAK_C = np.zeros((n,n))

a = compile_cls_cohs(CLS_C)
b = choose_coh_cls(a)
print b

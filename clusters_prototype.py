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
node_names = CLS_D['row_ids']
CLUSTS = load_clusters(open(clusts_fname))

# Convert cluster names into row IDs (indexed from zero)
C, clust_names = clust_names_to_row_num_list(CLUSTS, node_names)

CLS_C, CLS_Coh = compress_cls(C, CLS)
DCOR_U, DCOR_S = compress_dcor(C, DCOR)
WEAK_C = compress_weak(C, WEAK)

# save compressed matrices
# print cluster member lists
# plot clusters
# plot inter-clusters

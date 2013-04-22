from __future__ import division
from __init__ import *
import matrix_io as mio
from clusters_prototype_lib import *
import subprocess

min_d=0.30
cls_fname="data/D.expr.gold.CLS.apr.19.tab"
dcor_fname="data/D.expr.gold.DCOR.apr.19.tab"
color_fname="data/gold.celegans.phase.colors.genes.txt"
graphviz_cmd="dot"
weak_fname="data/gold.weak.tab"
outpath_prefix="~/Desktop/gold_0.30_cluster_proto"
clusts_fname="data/gold.k7.hclust.csv"
out_path="/Users/z/Desktop/"

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
node_styles = load_colors_as_node_style_dict(open("data/gold.cluster.colors.txt"))


node_names_np = np.array(node_names)
for i, vs in enumerate(C):
  clust_out = out_path+"%d.%s.clusts.dot" % (i,clust_names[i])
  idxs = list(vs)
  CLS_i = CLS[idxs,:][:,idxs]
  DCOR_i = DCOR[idxs,:][:,idxs]
  WEAK_i = WEAK[idxs,:][:,idxs]
  names_i = node_names_np[idxs]
  print '!!!', names_i, CLS_i, DCOR_i, WEAK_i
  G = print_graphviz(names=names_i, out=open(clust_out,"w"), CLS=CLS_i, DCOR=DCOR_i, WEAK=WEAK_i, min_d=0.3, weighted=True)
  cmd = "%s -T%s %s -o %s" % ("dot", "pdf", clust_out, clust_out+".pdf")
  print "Plotting graph using command [%s]..." % cmd
  print subprocess.call(cmd, shell=True)

CLS_C, CLS_Coh = compress_cls(C, CLS)
DCOR_U, DCOR_S = compress_dcor(C, DCOR)
WEAK_C = compress_weak(C, WEAK)

print CLUSTS
clust_out = out_path+"clusts.dot"
fp = open(clust_out,"w")
G = print_graphviz(names=clust_names, out=fp, CLS=CLS_C, DCOR=DCOR_U, WEAK=WEAK_C, min_d=0.3, weighted=True, node_styles=node_styles)
fp.close()
cmd = "%s -T%s %s -o %s" % ("dot", "pdf", clust_out, clust_out+".pdf")
print "Plotting graph using command [%s]..." % cmd
print subprocess.call(cmd, shell=True)

# TO FIX: remove node styles if nodes are missing. Abbr warning message
# TO FIX: plot single nodes without edges

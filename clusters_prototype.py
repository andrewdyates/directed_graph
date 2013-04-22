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
# NOTE: C is a list, not a dict. It is ordered.
C, clust_names = clust_names_to_row_num_list(CLUSTS, node_names)
node_styles = load_colors_as_node_style_dict(open("data/gold.celegans.phase.colors.genes.txt"))
print node_styles

C_plots = [] # cluster plot meta
node_names_np = np.array(node_names)
for i, vs in enumerate(C):
  clust_name = clust_names[i]
  clust_out = out_path+"clustnum_%d.clustname_%s.clusts.dot" % (i,clust_name)
  idxs = list(vs)
  CLS_i = CLS[idxs,:][:,idxs]
  DCOR_i = DCOR[idxs,:][:,idxs]
  WEAK_i = WEAK[idxs,:][:,idxs]
  names_i = node_names_np[idxs]
  G = print_graphviz(names=names_i, out=open(clust_out,"w"), CLS=CLS_i, DCOR=DCOR_i, WEAK=WEAK_i, min_d=0.3, weighted=True, prefix="margin=0;", node_styles=node_styles)
  figure_fname = clust_out+".pdf"
  cmd = "%s -T%s %s -o %s" % ("fdp", "pdf", clust_out, figure_fname)
  print "Plotting graph using command [%s]..." % cmd
  subprocess.call(cmd, shell=True)
  C_plots.append(get_pdf_file_size(figure_fname))

print "Subplot meta..."
print C_plots

CLS_C, CLS_Coh = compress_cls(C, CLS)
DCOR_U, DCOR_S = compress_dcor(C, DCOR)
WEAK_C = compress_weak(C, WEAK)

print CLUSTS
clust_out = out_path+"clusts.dot"
fp = open(clust_out,"w")
G = print_graphviz(names=clust_names, out=fp, CLS=CLS_C, DCOR=DCOR_U, WEAK=WEAK_C, min_d=0.3, weighted=False, node_styles=node_styles, cluster_sizes=C_plots)
fp.close()
cmd = "%s -T%s %s -o %s" % ("dot", "pdf", clust_out, clust_out+".pdf")
print "Plotting graph using command [%s]..." % cmd
print subprocess.call(cmd, shell=True)

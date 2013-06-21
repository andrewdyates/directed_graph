#!/usr/bin/python
"""Hack for custom cluster merging of BRCA E2F project."""
from __future__ import division
from __init__ import *
import matrix_io as mio
from clusters_prototype_lib import *
import subprocess

min_d=0.13
TAB_PREFIX="/Users/z/Dropbox/biostat/brca/GSE7307.e2fnets.jun19/tab/"
cls_fname=TAB_PREFIX+"jun20.R.GSE7307.TF.BOOL.syms.tab"
dcor_fname=TAB_PREFIX+"jun20.R.GSE7307.TF.DCOR.syms.tab"
weak_fname=TAB_PREFIX+"jun20.R.GSE7307.TF.WEAK.syms.tab"
graphviz_cmd="dot"
outpath_prefix="/Users/z/Desktop/brca_e2f_custom"
clusts_fname="/Users/z/Dropbox/biostat/brca/GSE7307.e2fnets.jun19/tab/jun19.GSE7307.k299.gsplom.clust.names.e2fcustom.txt"
out_path="/Users/z/Desktop/"

CLS_D = mio.load(cls_fname)
DCOR_D = mio.load(dcor_fname)
WEAK_D = mio.load(weak_fname)
CLS = CLS_D['M']
DCOR = DCOR_D['M']
WEAK = WEAK_D['M']
node_names = DCOR_D['row_ids']
CLUSTS = load_clusters(open(clusts_fname))
print CLS.shape, DCOR.shape, WEAK.shape

# Convert cluster names into row ID indices (indexed from zero)
# NOTE: C is a list, not a dict. It is ordered in same order as clust_names
C, clust_names = clust_names_to_row_num_list(CLUSTS, node_names)
print C
print clust_names

C_plots = [] # cluster plot meta
node_names_np = np.array(node_names)
do_fdp = set([0])
for i, vs in enumerate(C):
  clust_name = clust_names[i]
  clust_out = out_path+"clustnum_%d.clustname_%s.clusts.dot" % (i,clust_name)
  idxs = list(vs)
  CLS_i = CLS[idxs,:][:,idxs]
  DCOR_i = DCOR[idxs,:][:,idxs]
  WEAK_i = WEAK[idxs,:][:,idxs]
  names_i = node_names_np[idxs]
  
  if not i in do_fdp:
    G = print_graphviz(names=names_i, out=open(clust_out,"w"), CLS=CLS_i, DCOR=DCOR_i, WEAK=WEAK_i, min_d=0.13, weighted=False, prefix="margin=0;", spline="spline", rank_sep=0.3, node_sep=0.1)
    figure_fname = clust_out+".dot.pdf"
    cmd = "%s -T%s %s -o %s" % ("dot", "pdf", clust_out, figure_fname)
  else:
    # do_fdp
    G = print_graphviz(names=names_i, out=open(clust_out,"w"), CLS=CLS_i, DCOR=DCOR_i, WEAK=WEAK_i, min_d=0.13, weighted=True, prefix="margin=0;", spline="line")
    figure_fname = clust_out+".fdp.pdf"
    cmd = "%s -T%s %s -o %s" % ("fdp", "pdf", clust_out, figure_fname)
    
  print "Plotting graph using command [%s]..." % cmd
  subprocess.call(cmd, shell=True)
  C_plots.append(get_pdf_file_size(figure_fname))

print "File sizes in pixels:", C_plots

# select relevant sections of CLS, DCOR, WEAK
all_idxs = []
for vs in C:
  all_idxs += list(vs)
print "Gene idxes", all_idxs

names_s = list(node_names_np[all_idxs])
CLS_s = CLS[all_idxs,:][:,all_idxs]
DCOR_s = DCOR[all_idxs,:][:,all_idxs]
WEAK_s = WEAK[all_idxs,:][:,all_idxs]
print names_s
# remap cluster IDs
Cs = []
for c in C:
  Cs.append([names_s.index(node_names_np[cc]) for cc in c])
print Cs

# compress subselection
CLS_C, CLS_Coh = compress_cls(Cs, CLS_s)
DCOR_U, DCOR_S = compress_dcor(Cs, DCOR_s)
WEAK_C = compress_weak(Cs, WEAK_s)


print CLUSTS
clust_out = out_path+"clusts.dot"
fp = open(clust_out,"w")
G = print_graphviz(names=clust_names, out=fp, CLS=CLS_C, DCOR=DCOR_U, WEAK=WEAK_C, min_d=0.13, weighted=False, cluster_sizes=C_plots, rank_sep=0.4, node_sep=0.3)
fp.close()
cmd = "%s -T%s %s -o %s" % ("dot", "pdf", clust_out, clust_out+".pdf")
print "Plotting graph using command [%s]..." % cmd
print subprocess.call(cmd, shell=True)

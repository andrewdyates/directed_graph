#!/usr/bin/python
"""Hack script and notes to generate Jun19 BRCA network-of-networks.

python script.py min_d=0.30 cls_fname=data/D.expr.gold.CLS.apr.19.tab dcor_fname=data/D.expr.gold.DCOR.apr.19.tab color_fname=data/gold.celegans.phase.colors.genes.txt graphviz_cmd=dot weak_fname=data/gold.weak.tab weighted=False outpath_prefix=~/Desktop/gold_0.30_dot_nw

"""
from clusters_prototype_lib import *
import matrix_io as mio
import subprocess

DIR = "/Users/z/Dropbox/biostat/brca/GSE7307.e2fnets/"
PDF_PTN = DIR + "jun19_e2f_clust_pdfs/c%s.fdp.dot.pdf"
SUFFIXES = ['117', '150', '83', '82', '80', '51']
INTER_DCOR_D = mio.load(DIR+"GSE7307.TF.R.299.interest.inter.DCOR.jun19.tab")
INTER_BOOL_D = mio.load(DIR+"GSE7307.TF.R.299.interest.inter.BOOL.jun19.tab")
INTER_WEAK_D = mio.load(DIR+"GSE7307.TF.R.299.interest.inter.WEAK.jun19.tab")
print INTER_DCOR_D['row_ids']
print SUFFIXES
assert INTER_DCOR_D['row_ids'] == SUFFIXES
assert INTER_DCOR_D['row_ids'] == INTER_BOOL_D['row_ids']
assert INTER_DCOR_D['row_ids'] == INTER_WEAK_D['row_ids']
assert INTER_DCOR_D['row_ids'] == INTER_DCOR_D['col_ids']

C_plots = []
for c in SUFFIXES:
  print PDF_PTN%c
  w,h = get_pdf_file_size(PDF_PTN%c)
  C_plots.append((w,h))

clust_out = DIR+"e2f.jun20.clusts.dot"
fp = open(clust_out,"w")
G = print_graphviz(names=INTER_DCOR_D['row_ids'], out=fp, CLS=INTER_BOOL_D['M'], DCOR=INTER_DCOR_D['M'], WEAK=INTER_WEAK_D['M'], min_d=0.13, weighted=False, cluster_sizes=C_plots, node_sep=0.2)
fp.close()

cmd = "%s -T%s %s -o %s" % ("dot", "pdf", clust_out, clust_out+".pdf")
print "Plotting graph using command [%s]..." % cmd
print subprocess.call(cmd, shell=True)

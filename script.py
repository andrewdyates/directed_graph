#!/usr/bin/python
"""Practical wrapper around module to generate graphviz graphs.

EXAMPLE USE:
python script.py min_d=0.33 cls_fname=data/D.expr.gold.CLS.apr.19.tab dcor_fname=data/D.expr.gold.DCOR.apr.19.tab outpath_prefix=~/Desktop/gold_0.33 color_fname=data/gold.celegans.phase.colors.genes.txt

python script.py min_d=0.33 cls_fname=data/D.expr.gold.CLS.apr.19.tab dcor_fname=data/D.expr.gold.DCOR.apr.19.tab outpath_prefix=~/Desktop/gold_0.33_nw color_fname=data/gold.celegans.phase.colors.genes.txt weighted=False

python script.py min_d=0.33 cls_fname=data/D.expr.gold.CLS.apr.19.tab dcor_fname=data/D.expr.gold.DCOR.apr.19.tab outpath_prefix=~/Desktop/gold_0.33_fdp color_fname=data/gold.celegans.phase.colors.genes.txt graphviz_cmd=fdp

# with weaks, fdp
python script.py min_d=0.30 cls_fname=data/D.expr.gold.CLS.apr.19.tab dcor_fname=data/D.expr.gold.DCOR.apr.19.tab outpath_prefix=~/Desktop/gold_0.30_fdp color_fname=data/gold.celegans.phase.colors.genes.txt graphviz_cmd=fdp weak_fname=data/gold.weak.tab

# with weaks, no weight, dot
python script.py min_d=0.30 cls_fname=data/D.expr.gold.CLS.apr.19.tab dcor_fname=data/D.expr.gold.DCOR.apr.19.tab color_fname=data/gold.celegans.phase.colors.genes.txt graphviz_cmd=dot weak_fname=data/gold.weak.tab weighted=False outpath_prefix=~/Desktop/gold_0.30_dot_nw

# with weaks, weights, dot
python script.py min_d=0.30 cls_fname=data/D.expr.gold.CLS.apr.19.tab dcor_fname=data/D.expr.gold.DCOR.apr.19.tab color_fname=data/gold.celegans.phase.colors.genes.txt graphviz_cmd=dot weak_fname=data/gold.weak.tab outpath_prefix=~/Desktop/gold_0.30_dot

# ALL TRANS
# with weaks, weights, fdp (generates hairball)
python script.py min_d=0.30 cls_fname=data/trans.cls.tab dcor_fname=data/trans.dcor.tab color_fname=data/gold.celegans.phase.colors.genes.txt graphviz_cmd=fdp weak_fname=data/trans.weak.tab outpath_prefix=~/Desktop/alltrans_0.30_fdp

# with weaks, weights, fdp
python script.py min_d=0.8 cls_fname=data/trans.cls.tab dcor_fname=data/trans.dcor.tab color_fname=data/gold.celegans.phase.colors.genes.txt graphviz_cmd=fdp weak_fname=data/trans.weak.tab outpath_prefix=~/Desktop/alltrans_0.8_fdp

# ----------------------------------------
python script.py min_d=0.32 cls_fname=data/D.expr.gold.CLS.apr.19.tab dcor_fname=data/D.expr.gold.DCOR.apr.19.tab color_fname=data/gold.celegans.phase.colors.genes.txt graphviz_cmd=dot weak_fname=data/gold.weak.tab weighted=False outpath_prefix=~/Desktop/gold_0.32_dot_nw

python script.py min_d=0.36 cls_fname=data/D.expr.gold.CLS.apr.19.tab dcor_fname=data/D.expr.gold.DCOR.apr.19.tab color_fname=data/gold.celegans.phase.colors.genes.txt graphviz_cmd=dot weak_fname=data/gold.weak.tab weighted=False outpath_prefix=~/Desktop/gold_0.36_dot_nw

# -----------------------------------------
# attempt to plot C9 k=18 all trans clusters
python script.py min_d=0.32 cls_fname=data/all.trans.k18.C9.CLS.apr28.tab dcor_fname=data/all.trans.k18.C9.DCOR.apr28.tab color_fname=data/gold.celegans.phase.colors.genes.txt graphviz_cmd=fdp weighted=True outpath_prefix=~/Desktop/all_C9_0.32_fdp

python script.py min_d=0.32 cls_fname=data/all.trans.k18.C9.CLS.apr28.tab dcor_fname=data/all.trans.k18.C9.DCOR.apr28.tab color_fname=data/gold.celegans.phase.colors.genes.txt graphviz_cmd=dot weighted=False outpath_prefix=~/Desktop/all_C9_0.32_dot_nw

python script.py min_d=0.4 cls_fname=data/all.trans.k18.C9.CLS.apr28.tab dcor_fname=data/all.trans.k18.C9.DCOR.apr28.tab color_fname=data/gold.celegans.phase.colors.genes.txt graphviz_cmd=dot weighted=False outpath_prefix=~/Desktop/all_C9_0.4_dot_nw

# ----------------------------------------
# ATTEMPT TO PLOT k61 one iteration compressed clusters
# ----------------------------------------
python script.py min_d=0.32 cls_fname=data/all.trans.k61.CLS.apr28.tab dcor_fname=data/all.trans.k61.DCOR.apr28.tab color_fname=data/gold.celegans.phase.colors.genes.txt graphviz_cmd=dot weighted=False outpath_prefix=~/Desktop/all_k61_0.32_dot_nw

python script.py min_d=0.4 cls_fname=data/all.trans.k61.CLS.apr28.tab dcor_fname=data/all.trans.k61.DCOR.apr28.tab color_fname=data/gold.celegans.phase.colors.genes.txt graphviz_cmd=dot weighted=False outpath_prefix=~/Desktop/all_k61_0.4_dot_nw

python script.py min_d=0.5 cls_fname=data/all.trans.k61.CLS.apr28.tab dcor_fname=data/all.trans.k61.DCOR.apr28.tab color_fname=data/gold.celegans.phase.colors.genes.txt graphviz_cmd=dot weighted=False outpath_prefix=~/Desktop/all_k61_0.5_dot_nw

# include weak directions
python script.py min_d=0.5 weak_fname=data/all.trans.k61.WEAK.apr28.tab cls_fname=data/all.trans.k61.CLS.apr28.tab dcor_fname=data/all.trans.k61.DCOR.apr28.tab color_fname=data/gold.celegans.phase.colors.genes.txt graphviz_cmd=dot weighted=False outpath_prefix=~/Desktop/all_k61_0.5_dot_nw_weaks

# force layout
python script.py min_d=0.5 weak_fname=data/all.trans.k61.WEAK.apr28.tab cls_fname=data/all.trans.k61.CLS.apr28.tab dcor_fname=data/all.trans.k61.DCOR.apr28.tab color_fname=data/gold.celegans.phase.colors.genes.txt graphviz_cmd=fdp weighted=True outpath_prefix=~/Desktop/all_k61_0.5_fdp_weaks

python script.py min_d=0.6 weak_fname=data/all.trans.k61.WEAK.apr28.tab cls_fname=data/all.trans.k61.CLS.apr28.tab dcor_fname=data/all.trans.k61.DCOR.apr28.tab color_fname=data/gold.celegans.phase.colors.genes.txt graphviz_cmd=fdp weighted=True outpath_prefix=~/Desktop/all_k61_0.6_fdp_weaks

python script.py min_d=0.6 weak_fname=data/all.trans.k61.WEAK.apr28.tab cls_fname=data/all.trans.k61.CLS.apr28.tab dcor_fname=data/all.trans.k61.DCOR.apr28.tab color_fname=data/gold.celegans.phase.colors.genes.txt graphviz_cmd=dot weighted=False outpath_prefix=~/Desktop/all_k61_0.6_dot_nw_weaks
"""
import matrix_io as mio
from __init__ import *
import sys
import subprocess


def matrix_files_to_flat_graphviz_file(cls_fname=None, dcor_fname=None, out_fname=None, color_fname=None, weak_fname=None, min_d=0, weighted=True, plot_na=False, **kwds):
  """From matrix file names and parameters, write resulting graphviz output to file."""
  assert cls_fname and dcor_fname and out_fname
  weighted = str_true_false(weighted)
  plot_na = str_true_false(plot_na)
  min_d = float(min_d)
  assert min_d >= 0
  
  CLS_D = mio.load(cls_fname)
  DCOR_D = mio.load(dcor_fname)
  if color_fname:
    node_styles = load_colors_as_node_style_dict(open(color_fname))
  else:
    node_styles = None
  assert CLS_D['row_ids'] == CLS_D['col_ids']
  assert DCOR_D['row_ids'] == DCOR_D['col_ids']
  assert CLS_D['row_ids'] == DCOR_D['row_ids']
  names = CLS_D['row_ids']
  CLS, DCOR = CLS_D['M'], DCOR_D['M']
  assert np.size(CLS,0) == np.size(CLS,1)
  assert np.shape(CLS) == np.shape(DCOR)
  
  if weak_fname:
    WEAK_D = mio.load(weak_fname)
    assert WEAK_D['row_ids'] == WEAK_D['col_ids']
    assert WEAK_D['row_ids'] == names
    WEAK = WEAK_D["M"]
    assert np.shape(WEAK) == np.shape(CLS)
  else:
    WEAK = None
  
  out = open(out_fname, "w")
  G = print_graphviz(names=names, out=out, CLS=CLS, DCOR=DCOR, WEAK=WEAK, node_styles=node_styles, min_d=min_d, weighted=weighted, plot_na=plot_na, **kwds)
  out.close()
  return G

  
def make_and_compile(outpath_prefix=None, output_type="pdf", graphviz_cmd="dot", **kwds):
  assert outpath_prefix
  out_fname = outpath_prefix+".dot"
  print "Generating graphviz .dot text file as %s..." % out_fname
  G = matrix_files_to_flat_graphviz_file(out_fname=out_fname, **kwds)
  D = edge_list_to_adjMs(G)
  
  adj_fname = outpath_prefix+".adj.csv"  
  print "Saving graph adjacency matrix to file, col source to row, to %s" % adj_fname
  adjM_to_out(open(adj_fname,"w"), D['Adj'].T, D['nodes'])

  weak_fname = outpath_prefix+".weak.csv"  
  print "Saving graph weak flag to file, col source to row, to %s" % weak_fname
  adjM_to_out(open(weak_fname,"w"), D['Weak'].T, D['nodes'])

  cor_fname = outpath_prefix+".cor.csv"  
  print "Saving graph PC glyph correlated flag to file, col source to row, to %s" % cor_fname
  adjM_to_out(open(cor_fname,"w"), D['Cor'].T, D['nodes'])
  
  plot_fname = "%s.%s" % (out_fname, output_type)
  cmd = "%s -T%s %s -o %s" % (graphviz_cmd, output_type, out_fname, plot_fname)
  print "Plotting graph using command [%s]..." % cmd
  subprocess.call(cmd, shell=True)
  


if __name__ == "__main__":
  kwds = dict([(s.partition('=')[0],s.partition('=')[2]) for s in sys.argv[1:]])
  print kwds
  make_and_compile(**kwds)
  

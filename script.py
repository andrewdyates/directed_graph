#!/usr/bin/python
"""Practical wrapper around module to generate graphviz graphs.

EXAMPLE USE:
python script.py min_d=0.33 cls_fname=data/D.expr.gold.CLS.apr.19.tab dcor_fname=data/D.expr.gold.DCOR.apr.19.tab outpath_prefix=~/Desktop/gold_0.33 color_fname=data/gold.celegans.phase.colors.genes.txt
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
  print_graphviz(names=names, out=out, CLS=CLS, DCOR=DCOR, WEAK=WEAK, node_styles=node_styles, min_d=min_d, weighted=weighted, plot_na=plot_na, **kwds)
  out.close()
  return out_fname
  
def make_and_compile(outpath_prefix=None, output_type="pdf", graphviz_cmd="dot", **kwds):
  assert outpath_prefix
  out_fname = outpath_prefix+".dot"
  print "Generating graphviz .dot text file as %s..." % out_fname
  matrix_files_to_flat_graphviz_file(out_fname=out_fname, **kwds)
  plot_fname = "%s.%s" % (out_fname, output_type)
  cmd = "%s -T%s %s -o %s" % (graphviz_cmd, output_type, out_fname, plot_fname)
  print "Plotting graph using command [%s]..." % cmd
  r = subprocess.call(cmd, shell=True)
  print r


if __name__ == "__main__":
  kwds = dict([s.split('=') for s in sys.argv[1:]])
  print kwds
  make_and_compile(**kwds)
  
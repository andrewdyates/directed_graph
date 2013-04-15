"""
Make PCC undirected graph

python make_undirected.py > gold.w.undirected.dot
fdp -Tpdf gold.w.undirected.dot -o gold.w.undirected.dot.pdf
"""

import numpy as np
import matrix_io as mio
import sys

EDGES = '"%s" -- "%s"'
FONT_STRING = """
graph [fontname = "helvetica"];
node [fontname = "helvetica"];
edge [fontname = "helvetica", penwidth=1];"""

def load_colors(fname):
  q = [s.strip('\n\r').split(';') for s in open(fname) if len(s)>0 and s[0]!="#"]
  return dict(q)

def main(weighted=True, min_r=0.4):
  if isinstance(weighted, basestring) and weighted.lower() in ("f", "false", "0", "na","null"):
    weighted = False
  min_r = float(min_r)
  PCC = mio.load("data/gold.celegans.gse2180.pcc.csv")
  COLORS = load_colors("data/gold.celegans.gse2180.phase.colors.txt")
  
  print "graph {"
  print FONT_STRING
  if COLORS:
    for k,v in COLORS.items():
      print '"%s"[color="%s",style=filled,fontcolor=white]' % (k, v)
  for edge in undirected_ppc_edge(PCC, min_r, weighted):
    print edge
  print "}"
    
def undirected_ppc_edge(PCC, min_r=0.4, weighted=True):
  names = PCC['row_ids']
  n = np.shape(PCC['M'])[0]
  
  for i in xrange(n-1):
    for j in xrange(i+1, n):
      e = ""; r = PCC['M'][i,j]
      if r < min_r:
        continue
      if weighted:
        q = {'weight':"%f"%r}
      else:
        q = {}
      e = EDGES % (names[i], names[j])
      s = e + "[%s];" % ", ".join(["%s=%s"%(k,v) for k,v in q.items()])
      yield s
        
if __name__ == "__main__":
  main(**dict([s.split('=') for s in sys.argv[1:]]))

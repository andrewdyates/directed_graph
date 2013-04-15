#!/usr/bin/python
"""
python csvs_to_graphviz_summ_proto.py weighted=False colored=True > gold.nw.color.1.dot
dot -Tpdf gold.nw.color.1.dot -o gold.nw.color.1.dot.pdf

"""
import numpy as np
import matrix_io as mio
import sys


EDGES = '"%s" -> "%s"'
FONT_STRING = """
graph [fontname = "helvetica"];
node [fontname = "helvetica"];
edge [fontname = "helvetica", penwidth=1];"""

def load_colors(fname):
  q = [s.strip('\n\r').split(';') for s in open(fname) if len(s)>0 and s[0]!="#"]
  return dict(q)

def main(weighted=True, min_d=0.4, colored=False):
  if isinstance(weighted, basestring) and weighted.lower() in ("f", "false", "0", "na","null"):
    weighted = False
  if isinstance(colored, basestring) and colored.lower() in ("f", "false", "0", "na","null"):
    colored = False
  min_d = float(min_d)
  CLS = mio.load("data/gold.celegans.gse2180.cls.csv")
  DCOR = mio.load("data/gold.celegans.gse2180.dcor.csv")
  if colored:
    colors = load_colors("data/gold.celegans.gse2180.phase.colors.txt")
  else:
    colors = None
  print "digraph {"
  print FONT_STRING
  if colors:
    for k,v in colors.items():
      print '"%s"[color="%s",style=filled,fontcolor=white]' % (k, v)
  for edge in csv_to_graphvis(CLS, DCOR, min_d, weighted=weighted):
    print edge
  print "}"

def penwidth(c,d):
  if c==1 or c==3 or c==4:
    if d > 0.85:
      return "1.5"
    else:
      return "1.0"
  elif c == 2:
    if d > 0.9:
      return "2.5"
    elif d > 0.8:
      return "2.0"
    else:
      return "1.5"
  else:
    return "1.0"

def edgecolor(c,d):
  if c == 2:
    if d > 0.9:
      return "#2688bf"
    elif d > 0.8:
      return "#4197c7"
    else:
      return "#64acd4"
  else:
    return "#222222"
      
def csv_to_graphvis(CLS, DCOR, min_d=0.4, weighted=True, norm_weights=False):
  """GENERATOR: Convert symmetric adjancency matrices to directed graph"""
  assert type(CLS) == type(DCOR) == dict # matrix_io load dict
  assert CLS['row_ids'] == CLS['col_ids'] == DCOR['row_ids'] == DCOR['col_ids']
  assert np.shape(DCOR['M']) == np.shape(CLS['M'])
  assert np.shape(CLS['M'])[0] == np.shape(CLS['M'])[1]

  names = CLS['row_ids']
  n = np.shape(CLS['M'])[0]
  for i in xrange(n-1):
    for j in xrange(i+1, n):
      e = ""; c = CLS['M'][i,j]; d = DCOR['M'][i,j]
      if d <= min_d:
        continue
      else:
        if norm_weights:
          w = (d-min_d)/(1-min_d)
        else:
          w = d
      if weighted:
        q = {'weight':"%f"%w}
      else:
        q = {}
      if c == 1:
        e = EDGES % (names[i], names[j])
        q.update({"penwidth":penwidth(c,d), "color":'"%s"'%edgecolor(c,d)})
      elif c == 2:
        e = EDGES % (names[i], names[j])
        q.update({'dir':"none", "color":'"%s"'%edgecolor(c,d), "constraint":"false", "penwidth":penwidth(c,d)})
      elif c == 3:
        e = EDGES % (names[j], names[i])
        q.update({"penwidth":penwidth(c,d), "color":'"%s"'%edgecolor(c,d) })
      elif c == 4:
        e = EDGES % (names[i], names[j])
        q.update({'dir':"none", "color":'"#888888"', "constraint":"false", "style":"dashed"})
        q.update({"penwidth":penwidth(c,d)})
      elif c == 0:
        e = EDGES % (names[i], names[j])
        q.update({'dir':"none", "color":"#cccccc", "constraint":"false", "style":"dotted"})
      else:
        # 5,6,7 negative edges
        continue
      s = e + "[%s];" % ", ".join(["%s=%s"%(k,v) for k,v in q.items()])
      yield s
      

if __name__ == "__main__":
  args = dict([s.split('=') for s in sys.argv[1:]])
  main(**args)

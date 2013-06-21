#!/usr/bin/python
"""Convert matrices into graphviz .dot files.
"""
from __future__ import division
import numpy as np
import sys

# boolean class enumation key
BOOL_ENUM = {0:'NA', 1:'XiY', 2:'PC', 3:'YiX', 4:'UNL', 5:'MX', 6:'NC', 7:'OR', 8:'NA'}
# 0: no class; 1: and; 2: rn4c (row necessary for col); 3: cn4r (col necessary for row); 4: xor; 5: mix
WEAK_ENUM = {0:'nc', 1:'and', 2:'rn4c', 3:'cn4r', 4:'xor', 5:'mix'}

# GRAPHVIZ TEMPLATES
FONT_STRING = """graph [fontname = "helvetica", nodesep=%f, splines=%s, ranksep=%f, rank=same];
node [fontname = "helvetica", color="#000000", style=filled, fillcolor="#ffffff"];
edge [fontname = "helvetica", penwidth=1];"""

def load_rank_clusters(fp, clust_names=None):
  C = []
  for line in fp:
    line = line.strip()
    if not line: continue
    c = eval(line)
    for q in c:
      if not clust_names:
        C.append(q)
      else:
        qq = [clust_names[int(x)-1] for x in q]
        C.append(qq)
  return C

def str_true_false(s):
  if not s:
    return False
  if isinstance(s,basestring) and s.lower() in ("f","false","none","null"):
    return False
  return True

def load_clusters(fp):
  """Load cluster node_name,enumeration from csv file pointer."""
  C = {}
  for line in fp:
    name, enum = (s.strip('" ') for s in line.strip('\r\n').split(','))
    C.setdefault(enum,set()).add(name)
  return C

def load_colors_as_node_style_dict(fp):
  """Load fp of ;-delimited node name to #xxxxxx color mappings as node style dict."""
  q = {}
  for s in fp:
    s = s.strip("\n\r")
    if not (len(s)>0 and s[0]!="#"): continue
    node, color = s.split(';')
    q[node] = {'fillcolor':color, 'color':color}
  return dict(q)

def node_style_dict_to_str(d, is_filled=True):
  """Return graphviz string for node style dict."""
  if is_filled:
    d.setdefault("style", "filled")
    d.setdefault("fontcolor", "white")
  s = ", ".join(('%s="%s"'%(k,v) for k,v in d.items()))
  return s

def edge_list_to_adjM_dict(G):
  """Return A[source][dest] adj matrix."""
  A = {}
  nodes = G['nodes']
  for s in sorted(nodes):
    A[s] = {}
  for e in G['edges']:
    s,d = e['source'], e['dest']
    A[s][d] = e
    if not e['directed']:
      A[d][s] = e
  return A

def edge_list_to_adjMs(G):
  """Export graph dict returned from print_graphviz to adj matrices."""
  A = edge_list_to_adjM_dict(G)
  nodes = G['nodes']
  node_idx = dict(( (s,i) for i,s in enumerate(nodes) ))
  n = len(nodes)
  Adj = np.zeros((n,n), dtype=np.bool)
  Weak = np.zeros((n,n), dtype=np.bool)
  Cor = np.zeros((n,n), dtype=np.bool)
  for s in A:
    for d,e in A[s].items():
      i,j = node_idx[s], node_idx[d]
      Adj[i,j] = True
      if e['cls'] == 2:
        Cor[i,j] = True; Cor[j,i] = True
      if e['cls'] == 4:
        Weak[i,j] = True; Weak[j,i] = True
  return {'Adj':Adj, 'nodes':nodes, 'Cor':Cor, 'Weak':Weak}

def adjM_to_out(out, Adj, nodes):
  """Print Adjacency matrix to out as csv."""
  print >>out, ",".join([""]+nodes)
  for i, row in enumerate(Adj):
    r = [str(int(r)) for r in row]
    print >>out, ",".join([nodes[i]]+r)
  
def get_adj_dict(names, CLS, DCOR, WEAK=None):
  G = {'nodes':names, 'edges':[]}
  if len(names) > 1:
    for d in yield_matrix_to_edge_dict(names=names, CLS=CLS, DCOR=DCOR, WEAK=WEAK):
      if d:
        G['edges'].append(d)
  return G

    
def print_graphviz(names, out=sys.stdout, node_styles=None, graph_type="digraph", prefix="", postfix="", cluster_sizes=None, rank_clusters=None, ignore_nodes=None, weak_orders=True, spline="ortho", node_sep=0, rank_sep=0.7, **kwds):
  """Print graphviz output to `out` stream.
  Return dict of edge and node representation
  See `yield_matrix_to_edge_dict` for additional options passed via **kwds.
  """
  #print kwds['IGNORE']
  node_sep = float(node_sep)
  rank_sep = float(rank_sep)
  # Print header.
  print >>out, "%s {" % (graph_type)
  if prefix: print >>out, prefix
  print >>out, FONT_STRING % (node_sep, spline, rank_sep)
  # strip double quotes in node names
  if ignore_nodes is not None:
    ignore_nodes = set(ignore_nodes)
  else:
    ignore_nodes = set()
  names = [s.strip('"') for s in names]
  # Flag for plotting as clusters or not.
  as_clusters = cluster_sizes is not None
  # Print node list, add style if it exists.
  for i, node_name in enumerate(names):
    if node_name in ignore_nodes:
      continue
    if as_clusters:
      # default pdf dpi is 72px/in
      w,h=cluster_sizes[i]
      style_d = {'width': str(w/72), 'height':str(h/72), 'shape':'box', 'peripheries':'2'}
    else:
      style_d = {}
    if node_styles is not None and node_name in node_styles:
      style_d.update(node_styles[node_name])
    if style_d:
      print >>out, '"%s" [%s];' % (node_name, node_style_dict_to_str(style_d, not as_clusters))
    else:
      print >>out, '"%s";' % (node_name)
  # Print node groupings
  if rank_clusters is not None:
    for i,c in enumerate(rank_clusters):
      print >>out, subgraph_string(c,i,ignore_nodes)
    
  # Print edges
  G = {'nodes':names, 'edges':[]}
  if len(names) > 1:
    for d in yield_matrix_to_edge_dict(names=names, as_clusters=as_clusters, **kwds):
      if d:
        print >>out, edge_attr_to_line(d)
        G['edges'].append(d)
  # Print footer.
  if postfix: print >>out, postfix
  print >>out, "}"
  return G

def subgraph_string(c,i,ignore_nodes=None):
  if ignore_nodes is None:
    ignore_nodes = []
  s = []
  s += ["subgraph cluster_%d {"%i]
  if len(c) > 1:
    s += ['style=filled;\n color="#dddddd";']
  else:
    s += ['style=invis']
  for name in c:
    if name not in ignore_nodes:
      s += ['"%s";'%str(name)]
  s += ["}"]
  return "\n".join(s)
  
def yield_matrix_to_edge_dict(names=None, CLS=None, DCOR=None, WEAK=None, IGNORE=None, min_d=0.3, weighted=True, plot_na=False, as_clusters=False, weak_orders=True, **kwds):
  """Yield graphviz edge dict from adj matrices and list of names. Return None if no edge."""
  assert names is not None and CLS is not None and DCOR is not None
  assert np.size(CLS,0) == np.size(CLS,1)
  assert np.shape(CLS) == np.shape(DCOR)
  assert len(names) == np.size(CLS,0)
  if WEAK is not None:
    assert np.shape(CLS) == np.shape(WEAK)
  n = np.size(CLS,0)
  assert n>1
  for i in xrange(n-1):
    for j in xrange(i+1,n):
      cls, dcor = CLS[i,j], DCOR[i,j]
      if WEAK is not None:
        weak = WEAK[i,j]
      else:
        weak = None
      if IGNORE is not None:
        ignore = bool(IGNORE[i,j]) | bool(IGNORE[j,i]) # IGNORE is not a symmetric matrix! ignore any edge, not just directional!
      else:
        ignore = None
      if weighted:
        weight = dcor
      else:
        weight = None
      d = get_edge_dict(\
            rowname=names[i], colname=names[j], cls=cls, dcor=dcor, ignore=ignore,\
            weak_cls=weak, min_dcor=min_d, plot_na=plot_na, weight=weight, as_clusters=as_clusters,\
            weak_orders=weak_orders\
      )
      yield d

def edge_attr_to_line(d):
  """Given an edge dictionary generated by get_edge_dict, return graphviz string."""
  e = '"%s" -> "%s"' % (d['source'], d['dest'])
  a = ", ".join(("%s=%s"%(k,v) for k,v in d['attr'].items()))
  return "%s[%s];" % (e,a)
    
def get_edge_dict(rowname, colname, cls, dcor, weak_cls=None, ignore=None, min_dcor=0, plot_na=False, weight=None, as_clusters=False, weak_orders=False):
  """Return an attribute dict describing an edge. Return None if no edge."""
  assert cls in BOOL_ENUM.keys(); assert dcor >= 0 and dcor <= 1;
  assert min_dcor >= 0 and min_dcor <= 1
  assert rowname and colname
  if ignore is not None:
    assert ignore in (0,1,True,False)
  if weight is not None:
    if not isinstance(weight, basestring):
      weight = "%f"%weight
  
  # Edge Filtering
  # ------------------------------
  if not plot_na and (cls == 0 or cls == 8):
    return None
  if cls not in (0,1,2,3,4) and not as_clusters:
    return None
  if dcor < min_dcor:
    return None
    
  # Edge Direction
  # ------------------------------
  d = {'cls':int(cls), 'dcor':dcor, 'cluster_edge':as_clusters}
  if not weak_cls is None:
    d.update({'weak':int(weak_cls), 'is_weak':False})
  if cls == 1:
    d['source'] = rowname; d['dest'] = colname
    d['directed'] = True
  elif cls == 3: # edge goes opposite direction
    d['source'] = colname; d['dest'] = rowname
    d['directed'] = True
  elif cls == 4 and weak_cls is not None:
    # WEAK_ENUM = {0:'nc', 1:'and', 2:'rn4c', 3:'cn4r', 4:'xor', 5:'mix'}
    if weak_cls == 0 or weak_cls == 4: # no class or xor: no edge
      return None
    elif weak_cls == 3: # 3:cn4r
      d['source'] = colname; d['dest'] = rowname
      d['directed'] = True
      d['is_weak'] = True
    elif weak_cls == 2:
      d['directed'] = True
      d['source'] = rowname; d['dest'] = colname
      d['is_weak'] = True
    else:
      d['directed'] = False
      d['source'] = rowname; d['dest'] = colname
      d['is_weak'] = True
  else:
    # edge goes from row to column (or is undirected)
    d['source'] = rowname; d['dest'] = colname
    d['directed'] = False

  # Edge Attributes
  # ------------------------------
  d['attr'] = {"penwidth":penwidth(cls,dcor,scale=as_clusters), "color":'"%s"'%edgecolor(cls,dcor)}
  if weight is not None:
    d['attr']["weight"] = weight
  if cls == 0 or cls == 8:
    d['attr'].update({'dir':"none", "constraint":"false", "style":"dashed"})
  elif cls == 2:
    d['attr'].update({'dir':"none", "constraint":"false"})
  elif cls == 4:
    if weak_cls is not None:
      # necessary direction edges
      if weak_cls == 2 or weak_cls == 3:
        if weak_orders:
          d['attr'].update({"style":"dashed", "constraint":"true"})
        else:
          d['attr'].update({"style":"dashed", "constraint":"false"})
      else:
        d['attr'].update({'dir':"none", "constraint":"false", "style":"dashed"})
    else:
      d['attr'].update({'dir':"none", "constraint":"false", "style":"dashed"})
  elif cls in (5,6,7):
    d['attr'].update({'dir':"none", "constraint":"false"})
  elif cls in (1,3):
    pass
  else:
    raise Exception, "Unrecognized class %s" % cls

  # Make ignored edges invisible
  if ignore is not None and ignore:
    d['attr']['style'] = "invis"
      
  # RETURN EDGE DICT
  return d

def penwidth(c,d,scale):
  """Return an edge pen width string from class `c` and dcor `d`."""
  assert c in BOOL_ENUM.keys(); assert d >= 0 and d <= 1
  if c==1 or c==3 or c==4:
    if d > 0.85:   w = 1.5
    else:          w = 1.0
  elif c == 2:
    if d > 0.9:    w = 2.5
    elif d > 0.8:  w = 2.0
    else:          w = 1.5
  else:
    w = 1.0
  if scale:
    w = w*((1+d)**3)-0.5
  return "%f"%w

def edgecolor(c,d):
  """Return an edge color string from class `c` and dcor `d`."""
  assert c in BOOL_ENUM.keys(); assert d >= 0 and d <= 1
  if c == 0:
    return "#cccccc"
  elif c == 2:      # Positive Correlation (PC) class
    if d > 0.9:   return "#2688bf" # dark blue
    elif d > 0.8: return "#4197c7" # medium blue
    else:         return "#64acd4" # light blue
  elif c == 4:
    return "#999999"
  elif c == 5:
    return "#a00d42"
  elif c == 6:
    return "#d7424c"
  elif c == 7:
    return "#eb6532"
  else:           # All other edges
    return "#222222"   # almost black

def to_path_matrix(M, k=None):
  P = np.zeros(M.shape, dtype=np.int)
  for i in xrange(M.shape[1]):
    js = list(get_connected(M, i, k=k))
    P[js,i] = 1
  return P

def get_connected(M, s, k=None, lvl=0, visited=None):
  """Return set of all connected indices to s from column->row adj matrix."""
  if visited is None:
    visited=set()
  if k is not None and lvl >= k:
    return set()
  q = np.nonzero(M[:,s])[0]
  c = [i for i in q if i not in visited]
  v = visited.copy()
  v.update(c)
  for i in c:
    t = get_connected(M,i,k,lvl+1,v)
    v.update(t)
  return v
  

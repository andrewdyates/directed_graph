"""
Hack script to prune directed cluster graph.

dot -Tpdf ~/Dropbox/biostat/git_repos/directed_graph/data/all_k61_0.5_dot_nw_hack.dot -o /Users/z/Desktop/all_k61_0.5_dot_nw.dot.pdf

python summarize_summary_graphviz.py
"""
from __future__ import division
import paths
import numpy as np
import matrix_io as mio
import sys

ADJ_FNAME = "data/all_k61_0.5_dot_nw.adj.csv"
#ADJ_FNAME = "data/all_k61_0.5_dot_nw_ignores_weaks.adj.csv"
DOT_FNAME = "data/all_k61_0.5_dot_nw.dot"
RANKS_FNAME= "data/all_k61_0.5_dot_nw.dot.pdf_ranks.txt"
IGNORE_FNAME= "data/all_k61_0.5_dot_nw.adj.ignore.dcor65.csv"
DCOR_FNAME = "data/all.trans.k61.DCOR.apr28.tab"
DCOR_TH = 0.65

def main():
  # 1: load adj matrix
  ADJ_D = mio.load(ADJ_FNAME, dtype=np.int, force_row_ids=True, force_col_ids=True)
  DCOR_D = mio.load(DCOR_FNAME, force_row_ids=True, force_col_ids=True)
  assert len(ADJ_D['row_ids']) == len(ADJ_D['col_ids'])
  assert len(ADJ_D['row_ids']) == ADJ_D['M'].shape[0]
  assert DCOR_D["row_ids"] == ADJ_D['row_ids']
  assert DCOR_D["row_ids"] == DCOR_D["col_ids"]
  assert ADJ_D['M'].shape[0] == ADJ_D['M'].shape[1]
  n = ADJ_D['M'].shape[0]
  
  # 2.1: find paths k=2
  P2 = paths.fill_paths(ADJ_D["M"], k=2)
  mio.save(P2, open("data/all_k61_0.5_dot_nw.adj.paths.k2.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")
  # 2.2: find paths k=3
  P3 = paths.fill_paths(ADJ_D["M"], k=3)
  mio.save(P3, open("data/all_k61_0.5_dot_nw.adj.paths.k3.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")

  # 3.1: load ranks
  # (I compiled this list manually) Note that rank elements are 0 indexed in ADJ matrix
  ranks = load_ranks(open(RANKS_FNAME))
  # 3.2: load unconnected nodes 
  unconnected_nodes = ['53'] 
  node_clusters = []
  # 4: find clusters in same rank at k=2
  Ignore_Clust = np.zeros(ADJ_D['M'].shape, dtype=np.bool)
  for lvl, r in enumerate(ranks):
    CC = group_in_same_rank(r, P2)
    rnp = np.array(r)
    c = [map(str,rnp[cc]+1) for cc in CC]
    node_clusters.append(c)
    # Ignore edges in equal rank clusters
    for node in r:
      adj = set(np.nonzero(ADJ_D['M'][:,node])[0])
      for e in (adj & set(r)):
        Ignore_Clust[node,e] = True
        # Also remove corresponding opposite direction
        if ADJ_D['M'][node,e] == ADJ_D['M'][e,node] == 1:
          Ignore_Clust[e,node] = True

  print "Clusters"
  for c in node_clusters:
    print c
  print

  # 4.5 attempt to hide lower strength edges without disconnecting nodes
  DCOR = DCOR_D['M']
  AD = ADJ_D['M'].copy()
  Ignore_Low = np.zeros(ADJ_D['M'].shape, dtype=np.bool)
  for i in range(n):
    for j in range(n):
      if i == j: continue
      if DCOR[i,j] < DCOR_TH and AD[j,i]:
        # edge exists from i to j and it is under dCor thresh. can we remove it?
        AD[j,i] = 0
        # undirected edge
        if AD[i,j]:
          AD[i,j] = 0
          if np.sum(AD[:,i]) == 0 or np.sum(AD[j:,]) == 0 or \
             np.sum(AD[:,j]) == 0 or np.sum(AD[i:,]) == 0:
            # no, it disconnects something
            AD[i,j] = 1 
            AD[j,i] = 1
          else:
            Ignore_Low[i,j] = True
            Ignore_Low[j,i] = True
        # directed edge
        else:
          if np.sum(AD[:,i]) == 0 or np.sum(AD[j:,]) == 0:
            # no, it disconnects something
            AD[j,i] = 1
          else:
            Ignore_Low[j,i] = True
  NL = count_edges(Ignore_Low)
  assert np.sum(Ignore_Low & ADJ_D['M']) == np.sum(Ignore_Low)
  print "Too low:", NL
  

  # 5: look for redudant directed edges between levels at least 2 levels apart
  # remove edge if path of equal length already exists
  Ignore_Far = np.zeros(ADJ_D['M'].shape, dtype=np.bool)
  A = ADJ_D['M'].copy()
  A = A & (~Ignore_Low)
  n_far_edges = 0
  for lvl in xrange(len(ranks)-2):
    this_rank = ranks[lvl]
    for dlvl in xrange(lvl+2,len(ranks)):
      delta = dlvl-lvl
      that_rank = ranks[dlvl]
      for top in this_rank:
        for low in that_rank:
          if A[low,top]:     # adj is col->row
            n_far_edges += 1
            A[low,top] = 0 # try removing this link
            # is there an alternate path of equal length to this node?
            conn = paths.is_path(A,top,delta+1)
            if not low in conn:
              A[low,top] = 1 # I guess we need this edge...
            else:
              Ignore_Far[low,top] = True
              # also remove an associated undirected edge
              if A[top,low]:
                Ignore_Far[top,low] = True
                A[top,low] = 0
  print "# Far edges", n_far_edges

  # 6: Print Stats
  assert np.sum(Ignore_Clust & Ignore_Far)==0
  NT = count_edges(ADJ_D['M'])
  NS = count_edges(Ignore_Clust)
  NF = count_edges(Ignore_Far)
  print "Total:", NT
  print "Same Level:", NS
  print "Redundant Far:", NF
  n_rm = NS['total']+NF['total']+NL['total'] # this is wrong
  #$print "removed:", n_rm
  #print "reduction:", n_rm/NT['total']
  
  # 7: Save Edge Ignore Matrix
  Ignore = Ignore_Clust | Ignore_Far | Ignore_Low
  NI = count_edges(Ignore)
  print "Ignored", NI
  print np.sum(Ignore)
  print np.sum(Ignore_Clust | Ignore_Far)
    
  print "Save Ignore Matrix at:", IGNORE_FNAME
  mio.save(Ignore, open(IGNORE_FNAME, "w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")
  
  

def group_in_same_rank(r, P):
  """Return clique subsets."""
  A = P[r,:][:,r]
  n = len(r)
  # convert to reciprocal undirected graph
  for i in xrange(n-1):
    for j in xrange(i,n):
      e = A[i,j] & A[j,i]
      A[i,j] = e
      A[j,i] = e
  Pinf = paths.fill_paths(A)
  CC = connected_components(Pinf)
  return CC
  
def connected_components(U):
  """Return connected components of undirected graph."""
  n = U.shape[0]
  e = set(range(n))
  c = []
  while len(e):
    x = set([e.pop()])
    q = set(np.nonzero(U[:,list(x)])[0]) & e
    for z in q:
      x.add(z)
      e.remove(z)
    c.append(sorted(x))
  return c

def load_ranks(fp):
  """Load 1-idx ranks as list of 0-index sets of integers."""
  ranks = []
  for line in fp:
    line = line.strip()
    if not line: continue
    members = set([int(s)-1 for s in line.split(',')])
    ranks.append(sorted(members))
  return ranks

def count_edges(A):
  """Count edges in adjacency matrix."""
  assert A.shape[0] == A.shape[1]
  n = A.shape[0]
  n_directed = 0
  n_undirected = 0
  for i in xrange(n-1):
    for j in xrange(i+1,n):
      if A[i,j] and not A[j,i]:
        n_directed += 1
      elif not A[i,j] and A[j,i]:
        n_directed += 1
      elif A[i,j] and A[j,i]:
        n_undirected += 1
  total = n_directed + n_undirected
  n_filled = int(np.sum(A))
  return {'directed': n_directed, 'undirected': n_undirected, 'total': total, 'filled': n_filled}


    
if __name__ == "__main__":
  main()

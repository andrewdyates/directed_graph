ADJ_FNAME = "data/all_k61_0.5_dot_nw.adj.csv"
DOT_FNAME = "data/all_k61_0.5_dot_nw.dot"
RANKS_FNAME= "data/all_k61_0.5_dot_nw.dot.pdf_ranks.txt"
import paths
import numpy as np
import matrix_io as mio


def main():
  # 1: load adj matrix
  ADJ_D = mio.load(ADJ_FNAME, dtype=np.int, force_row_ids=True, force_col_ids=True)
  assert len(ADJ_D['row_ids']) == len(ADJ_D['col_ids'])
  assert len(ADJ_D['row_ids']) == ADJ_D['M'].shape[0]
  assert ADJ_D['M'].shape[0] == ADJ_D['M'].shape[1]

  # 2.1: find paths k=3
  P3 = paths.fill_paths(ADJ_D["M"], k=3)
  mio.save(P3, open("data/all_k61_0.5_dot_nw.adj.paths.k3.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")

  # 2.2: find paths k=2
  P2 = paths.fill_paths(ADJ_D["M"], k=2)
  mio.save(P2, open("data/all_k61_0.5_dot_nw.adj.paths.k2.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")

  # 3: load ranks
  ranks = load_ranks(open(RANKS_FNAME))

  # 4: find clusters in same rank at k=2
  for lvl, r in enumerate(ranks):
    #print lvl, r
    CC = group_in_same_rank(r, P2)
    rnp = np.array(r)
    #print CC
    print [map(str,rnp[cc]+1) for cc in CC]
      


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
    
if __name__ == "__main__":
  main()

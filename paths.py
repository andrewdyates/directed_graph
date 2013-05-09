import numpy as np

def fill_paths(M, k=None):
  P = np.zeros(M.shape, dtype=np.int)
  for i in xrange(M.shape[1]):
    js = list(get_connected(M, i, k=k))
    P[js,i] = 1
  return P

def is_path(M, s, k=None):
  """Return all nodes connected to node s by a directed path by d.

  M: column to row adj matrix
  """
  visited = set()
  queue = [(s,0)]
  while queue:
    r, lvl = queue.pop()
    if k is not None and lvl>k:
      continue
    if r not in visited:
      visited.add(r)
      q = np.nonzero(M[:,r])[0]
      z = [(i,lvl+1) for i in q if i not in visited]
      queue += z
  return visited

def get_connected(M, s, k=None, lvl=0, visited=None):
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

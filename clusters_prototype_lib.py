from __future__ import division
from __init__ import *

# BOOL_ENUM = {0:'NA', 1:'XiY', 2:'PC', 3:'YiX', 4:'UNL', 5:'MX', 6:'NC', 7:'OR'}
CLS_HAMM_DIST = np.array((
  (0,2,2,2,2,2,2,2), # NA
  (2,0,1,2,1,2,3,2), # XiY
  (2,1,0,1,2,3,4,3), # PC
  (2,2,1,0,1,2,3,2), # YiX
  (2,1,2,1,0,1,2,1), # UNL
  (2,2,3,2,1,0,1,2), # MX
  (2,3,4,3,2,1,0,1), # NC
  (2,2,3,2,1,2,1,0)  # OR
))

def clust_names_to_row_nums(C, names):
  Cnum = {}
  name_idx = dict( (s,i) for i,s in enumerate(names) )
  for k,vs in C.items():
    Cnum[k] = set((name_idx[s] for s in vs))
  return Cnum

def compile_cls_cohs(CLS, sym=True):
  """Compile boolean classes to coherence enum list."""
  assert np.size(CLS,0) == np.size(CLS,1)
  n = np.size(CLS,0)
  iu = np.triu_indices(n,1)
  #BOOL_ENUM = {0:'NA', 1:'XiY', 2:'PC', 3:'YiX', 4:'UNL', 5:'MX', 6:'NC', 7:'OR'}
  cls_cnts = [0]*8
  for enum in range(8):
    cls_cnts[enum] = np.sum(CLS[iu] == enum)
  # account for arbitrary symmetry across diagonal for XiY and YiX glyphs
  if sym:
    cls_cnts[1] = cls_cnts[1] + cls_cnts[3] 
    cls_cnts[3] = 0
  coh = np.array([-1.0]*8)
  for enum in range(8):
    coh[enum] = cls_coherence(cls_cnts, enum)
  return coh

def cls_coherence(counts, cls):
  """Return coherence for `cls` given `counts` of other classes.
  coherence is 1-(1/4) mean hamming distance to cls
  1 is best, 0 is worst."""
  assert len(counts) == 8
  assert sum(np.array(counts) < 0) == 0
  assert cls >= 0 and cls <= 7
  n = sum(counts)
  sigma = 0
  for enum, cnt in enumerate(counts):
    sigma += CLS_HAMM_DIST[enum,cls]*cnt
  return 1-(sigma/n/4)

def choose_coh_cls(coh, min_coh=0.7):
  """Given coh vector from compile_cls_coh, return most representative class."""
  max_coh = np.amax(coh)
  max_coh_i = coh == max_coh
  if max_coh < min_coh:
    return 4 # UNL
  if np.sum(max_coh_i) == 1:
    return np.arange(8)[max_coh_i][0]
  else:
    # Handle ties.
    # ------------------------
    # 1. ignore NA class
    if np.sum(max_coh_i[1:]) == 1:
      return coh[max_coh_i[1:]]
    # 2. if ties for opposite signs, set as UNL
    pos = np.array((0,1,1,1,0,0,0,0))
    neg = np.array((0,0,0,0,0,1,1,1))
    if any((max_coh_i & pos) & (max_coh_i & neg)):
      return 4
    # 3. if all of a sign or both asyms, return sym
    if all(max_coh_i[(1,3)]):
      return 2
    if all(max_coh_i[(5,7)]):
      return 6
    # 4. if an asym and sym of the same sign, return asym
    if max_coh_i[1]: return 1
    if max_coh_i[3]: return 3
    if max_coh_i[5]: return 5
    if max_coh_i[7]: return 7
    # Raise an exception if a class has not been chosen. Such is probably a bug.
    raise Exception, "Edge case: cannot choose most coherent class. %s" % coh

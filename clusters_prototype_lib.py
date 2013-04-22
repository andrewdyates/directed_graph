from __future__ import division
from __init__ import *

# BOOL_ENUM = {0:'NA', 1:'XiY', 2:'PC', 3:'YiX', 4:'UNL', 5:'MX', 6:'NC', 7:'OR'}
# WEAK_ENUM = 0: no class; 1: and; 2: rn4c; 3: cn4r; 4: xor; 5: mix
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

def get_comp_cls(CLS, sym=True, min_coh=0.7):
  """Helper function for returning compressed binary class."""
  c = compile_cls_cohs(CLS, sym=sym)
  max_coh = max(c)
  cls = choose_coh_cls(c, min_coh=min_coh)
  return cls, max_coh

def clust_names_to_row_num_list(C, names):
  """Given dict `C` of {name:set(node_names)}, convert to list of indices."""
  Cnum, clust_names = [], []
  name_idx = dict( (s,i) for i,s in enumerate(names) )
  for i, k in enumerate(sorted(C)):
    clust_names.append(k)
    vs = C[k]
    Cnum.append(set((name_idx[s] for s in vs)))
  return Cnum, clust_names

def compile_cls_cohs(CLS, sym=True):
  """Compile boolean classes to coherence enum list."""
  if sym:
    # upper triangle of square matrix only
    assert len(CLS.shape)==2 and CLS.shape[0] == CLS.shape[1]
    n = np.shape(CLS)[0]
    if n == 1:
      iu = 0
    else:
      iu = np.triu_indices(n,1)
  #BOOL_ENUM = {0:'NA', 1:'XiY', 2:'PC', 3:'YiX', 4:'UNL', 5:'MX', 6:'NC', 7:'OR'}
  cls_cnts = [0]*8
  for enum in range(8):
    if sym:
      cls_cnts[enum] = np.sum(CLS[iu] == enum)
    else:
      cls_cnts[enum] = np.sum(CLS == enum)
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
  max_coh_i = np.array(coh == max_coh)
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
    if all(max_coh_i[[1,3]]):
      return 2
    if all(max_coh_i[[5,7]]):
      return 6
    # 4. if an asym and sym of the same sign, return asym
    if max_coh_i[1]: return 1
    if max_coh_i[3]: return 3
    if max_coh_i[5]: return 5
    if max_coh_i[7]: return 7
    # Raise an exception if a class has not been chosen. Such is probably a bug.
    raise Exception, "Edge case: cannot choose most coherent class. %s" % coh

def compress_cls(CLUST_i, CLS, **kwds):
  """Compress boolean class matrix by coherence using existing clustering.

  Args:
    CLUST_i: [set(i)] of sets of indices in `CLS` corresponding to clusters
    CLS: np.array matrix of boolean class enumerations
  Returns:
    (COMP, COH) where:
      COMP: nxn compressed boolean class enumeration matrix, n = len(CLUST_i)
      COH: nxn corresponding coherence matrix
  """
  a, b = CLS.shape[0]-1, max((max(s) for s in CLUST_i))
  assert a==b, "Maximum cluster index %d != CLS matrix row index %d." % (a,b)
  n = len(CLUST_i)
  COMP = np.zeros((n,n))
  COH = np.zeros((n,n))
  for i in xrange(n):
    idxs_i = list(CLUST_i[i])
    for j in xrange(i,n):
      idxs_j = list(CLUST_i[j])
      C = CLS[idxs_i,:][:,idxs_j]
      cls, coh = get_comp_cls(C, sym=(i==j), **kwds)
      COMP[i,j] = cls
      COH[i,j], COH[j,i] = coh, coh
      if i!=j: # reflect assignment over diagonal
        if cls == 1:
          COMP[j,i] = 3
        elif cls == 3:
          COMP[j,i] = 1
        else: 
          COMP[j,i] = cls
  return COMP, COH

def get_mean_std_dcor(D, sym=True):
  """Return mean, std of dCor matrix."""
  if sym:
    # upper triangle of square matrix only
    assert len(D.shape)==2 and D.shape[0] == D.shape[1]
    n = np.shape(D)[0]
    if n == 1:
      iu = 0
    else:
      iu = np.triu_indices(n,1)
    u = np.mean(D[iu])
    s = np.std(D[iu])
  else:
    u = np.mean(D)
    s = np.std(D)
  return u, s

def compress_dcor(CLUST_i, DCOR):
  """Compress dCor matrix by mean.

  Args:
    CLUST_i: [set(i)] of sets of indices in `CLS` corresponding to clusters
    DCOR: np.array sym matrix of distance correlation
  Returns:
    (MEAN, STD) where:
      MEAN: nxn compressed cluster mean DCOR matrix, n = len(CLUST_i)
      STD: nxn corresponding standard deviation matrix
  """
  n = len(CLUST_i)
  MEAN = np.zeros((n,n))
  STD = np.zeros((n,n))
  for i in xrange(n):
    idxs_i = list(CLUST_i[i])
    for j in xrange(i,n):
      idxs_j = list(CLUST_i[j])
      D = DCOR[idxs_i,:][:,idxs_j]
      u, s = get_mean_std_dcor(D, sym=i==j)
      MEAN[i,j] = u; MEAN[j,i] = u;
      STD[i,j] = s; STD[j,i] = s;
  return MEAN, STD


# WEAK_ENUM = 0: no class; 1: and; 2: rn4c; 3: cn4r; 4: xor; 5: mix
def choose_weak(WEAK, sym=True, min_pct=0.4, over_mult=2):
  """Choose representative weak class."""
  if sym:
    # upper triangle of square matrix only
    assert len(WEAK.shape)==2 and WEAK.shape[0] == WEAK.shape[1]
    n = np.shape(WEAK)[0]
    if n == 1:
      iu = 0
    else:
      iu = np.triu_indices(n,1)
  
  weak_cnts = np.array([0]*6)
  for enum in range(6):
    if sym:
      weak_cnts[enum] = np.sum(WEAK[iu] == enum)
    else:
      weak_cnts[enum] = np.sum(WEAK == enum)
      
  i = np.argmax(weak_cnts)
  n = np.sum(weak_cnts)
  # no class meets threshold, return mixed(5)
  if i/n < min_pct:
    return 5
  # plurality class meets threshold and is non-directional, return it
  if i in (0,1,4,5):
    return i
  # plurality is directional, check that the other direction is comparatively rare.
  else:
    if i == 2:
      if weak_cnts[2] >= weak_cnts[3]*over_mult:
        return 2
      else:
        return 5
    if i == 3:
      if weak_cnts[3] >= weak_cnts[2]*over_mult:
        return 3
      else:
        return 5
    raise Exception, "Unknown case for weak cnts. This is probably a bug. %s" % weak_cnts
  
def compress_weak(CLUST_i, WEAK, **kwds):
  """Compress weak coupling matrix.
  """
  n = len(CLUST_i)
  COMP = np.zeros((n,n))
  for i in xrange(n):
    idxs_i = list(CLUST_i[i])
    for j in xrange(i,n):
      idxs_j = list(CLUST_i[j])
      W = WEAK[idxs_i,:][:,idxs_j]
      w = choose_weak(W, sym=i==j, **kwds)
      if w not in (2,3): # not directed
        COMP[i,j] = w; COMP[j,i] = w
      elif w == 2:
        COMP[i,j] = 2; COMP[j,i] = 3
      elif w == 3:
        COMP[i,j] = 3; COMP[j,i] = 2
  return COMP

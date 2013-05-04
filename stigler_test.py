#!/usr/bin/python
from __future__ import division
import matrix_io as mio
import numpy as np

def main():
  GOLD_D = mio.load("data/gold_standard_network.csv", dtype=str)
  MIM_D = mio.load("data/mim_msa_cov.csv", dtype=str)
  YATES_D = mio.load("data/gold_0.32_dot_nw.adj.csv", dtype=str)
  Y2_D = mio.load("data/gold.paths.dcor0.32.k2.tab", dtype=str)

  assert GOLD_D["row_ids"] == GOLD_D["col_ids"]
  assert MIM_D["row_ids"] == MIM_D["col_ids"]
  assert YATES_D["row_ids"] == YATES_D["col_ids"]
  assert GOLD_D["row_ids"] == MIM_D["row_ids"]
  assert Y2_D["row_ids"] == Y2_D["col_ids"]
  assert Y2_D["row_ids"] == YATES_D["row_ids"]

  # align YATES and GOLD
  GOLDi = [ YATES_D['row_ids'].index(x) if x in YATES_D['row_ids'] else None for x in GOLD_D['row_ids'] ]
  GOLDiy = filter(lambda s: s is not None, GOLDi)
  GOLDin = [i for i,s in enumerate(GOLDi) if s is not None]
  #print np.array(YATES_D['row_ids'])[GOLDiy]
  #print np.array(GOLD_D['row_ids'])[GOLDin]
  #print MIM_D['M']
  #print GOLD_D['M']

  #r = test(GOLD_D['M'], MIM_D['M'], GOLD_D['row_ids'])
  #print r
  # fp = open("/Users/z/Desktop/mim-cov.csv", "w")
  # fp.write(",".join([""]+GOLD_D['col_ids'])+"\n")
  # for i,row in enumerate(r['R']):
  #   fp.write(GOLD_D['row_ids'][i]+",")
  #   fp.write(",".join(row)+"\n")
  # fp.close()

  # COMPARE GOLD WITH MIM
  print "GOLD VS MIM"
  R_G_MIM = test_mods(GOLD_D['M'], MIM_D['M'], GOLD_D['row_ids'])
  print

  # COMPARE GOLD WITH YATES
  assert list(np.array(YATES_D['row_ids'])[GOLDiy]) == list(np.array(GOLD_D['row_ids'])[GOLDin])
  row_ids=list(np.array(GOLD_D['row_ids'])[GOLDin])
  print
  G = GOLD_D['M'][GOLDin,:][:,GOLDin]
  Y = YATES_D['M'][GOLDiy,:][:,GOLDiy]
  Y2 = Y2_D['M'][GOLDiy,:][:,GOLDiy]
  print "GOLD VS YATES EDGES"
  R_G_Y = test_mods(G,Y, row_ids)
  print
  
  print "GOLD VS YATES WITH PATHS"
  R_G_Y2 = test_mods(G,Y2,row_ids)
  print

  ### GENERATE TABLE

  
def test_mods(G,M,row_ids):
  assert G.shape == M.shape
  n = M.shape[0]
  pal1_i = [row_ids.index(x) for x in ["pal-1"]]
  ecto_i = [row_ids.index(x) for x in ["elt-1", "lin-26", "nhr-25", "elt-3"]]
  meso_i = [row_ids.index(x) for x in ["hnd-1", "hlh-1", "unc-120"]]
  r_overall = test(G,M,row_ids) # gold, model
  r_pal1 = test(G[:,pal1_i], M[:,pal1_i], row_ids, col_ids=["pal-1"])
  r_ecto = test(G[ecto_i,:], M[ecto_i,:], ["elt-1", "lin-26", "nhr-25", "elt-3"], row_ids)
  r_meso = test(G[meso_i,:], M[meso_i,:], ["hnd-1", "hlh-1", "unc-120"], row_ids)

  r_ecto_s = test(G[ecto_i,:][:,ecto_i], M[ecto_i,:][:,ecto_i], ["elt-1", "lin-26", "nhr-25", "elt-3"])
  r_meso_s = test(G[meso_i,:][:,meso_i], M[meso_i,][:,meso_i], ["hnd-1", "hlh-1", "unc-120"])
  # print r_meso
  # fp = open("/Users/z/Desktop/meso-mim-cov.csv", "w")
  # fp.write(",".join([""]+row_ids)+"\n")
  # for i,row in enumerate(r_meso['R']):
  #   fp.write(["hnd-1", "hlh-1", "unc-120"][i]+",")
  #   fp.write(",".join(row)+"\n")
  # fp.close()
  print "overall"
  print r_overall
  print
  print "pal1 targets"
  print r_pal1
  print
  print "ectoderm (w)"
  print r_ecto
  print
  print "ectoderm (s)"
  print r_ecto_s
  print
  print "mesoderm (w)"
  print r_meso
  print
  print "mesoderm (s)"
  print r_meso_s
  print
  return {'overall': r_overall, 'pal1': r_pal1, 'ecto': r_ecto,
          'ecto_s': r_ecto_s, 'meso': r_meso, 'meso_s': r_meso_s}

#Gold, model
def test(G,M,row_ids,col_ids=None,debug=False):
  if col_ids is None:
    col_ids = row_ids
  assert G.shape == M.shape
  nrow,ncol = M.shape[0], M.shape[1]
  R = [ ["-"]*ncol for i in xrange(nrow) ]
  tp, tn, fp, fn, hr = 0,0,0,0,0
  for i in xrange(nrow):
    for j in xrange(ncol):
      # if row_ids[i] == col_ids[j]:
      #   #continue
      #   g, m = G[i,j], "1"
      # else:
      #   g, m = G[i,j], M[i,j]
      g, m = G[i,j], M[i,j]
      if (m=="1" and g=="1") or (m=="1" and g=="-1") or (m=="-1" and g=="-1"):
        tp += 1
        R[i][j] = "TP"
      if m==g=="0":
        tn += 1
        R[i][j] = "TN"
      if m=="-1" and g=="1":
        hr += 1
        R[i][j] = "0.5"
      if m in ("1","-1") and g=="0":
        fp += 1
        R[i][j] = "FP"
      if m=="0" and g in ("1","-1"):
        fn += 1
        R[i][j] = "FN"
      if debug:
        print i,j
        print "\t".join([row_ids[i],col_ids[j],R[i][j],"m",m,"g",g])
  tpr = (tp+0.5*hr) / ((tp+0.5*hr)+(fn+0.5*hr)) # true positive rate or precision
  ppv = (tp + 0.5*hr) / ((tp+0.5*hr)+fp) # positive predictive value or recall
  total = tp+tn+hr+fp
  if fp+tn == 0:
    fpr = 0
  else:
    fpr = fp/(fp+tn) # false positive rate:
  try:
    chard = fp/(fp+fn) # incorrect computation of fpr
  except:
    chard = 0
  total_true = tp+tn+0.5*hr
  all_set = tp+tn+fp+fn+hr
  pc_dist = pr_space(ppv, tpr) # recall or ppv on x axis
  roc_dist = roc_space(fpr, tpr) # fpr on x axis, tpr on y axis
  chigger_dist = roc_space(chard, tpr) # fpr on x axis, tpr on y axis

  #accuracy.... sensitvity, specifcity
  acc = (tp+tn+(0.5*hr))/(tp+fp+fn+tn+hr)
  prec = (tp+(0.5)*hr)/(tp+fp+(0.5*hr))
  sens = (tp+(0.5)*hr) / (tp+(0.5)*hr+fn)
  try:
    spec = tn / (tn+fp)
  except:
    spec = 0
  
  return {'tp':tp,'tn':tn,'fp':fp,'fn':fn,'hr':hr,'tpr':tpr,'ppv':ppv,'total':total,'true':total_true,"R":R, 'all':all_set,'fpr':fpr, 'pc_dist': pc_dist, 'roc_dist':roc_dist, 'chard':chard, 'chigger': chigger_dist, 'acc':acc, 'prec':prec, 'sens':sens, 'spec':spec}


# x: fpr, y: tpr
def roc_space(x,y):
  return np.sqrt(2)*(y-x)/2

# x: recall, y: precision
def pr_space(x,y):
  if x < y:
    sign = -1
  else:
    sign = 1
  return sign * (np.sqrt(2)*((x-1)+y))/2
  
if __name__ == "__main__":
  main()

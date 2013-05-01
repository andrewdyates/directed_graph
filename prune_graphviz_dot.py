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

  # 2: find all paths
  Pinf = paths.fill_paths(ADJ_D["M"], k=None)
  mio.save(Pinf, open("data/all_k61_0.5_dot_nw.adj.paths.kinf.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")
  print np.sum(ADJ_D["M"]!=Pinf)
  
  P2 = paths.fill_paths(ADJ_D["M"], k=2)
  mio.save(P2, open("data/all_k61_0.5_dot_nw.adj.paths.k2.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")
  print np.sum(P2!=Pinf)
  
  P3 = paths.fill_paths(ADJ_D["M"], k=3)
  mio.save(P3, open("data/all_k61_0.5_dot_nw.adj.paths.k3.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")
  print np.sum(P3!=Pinf)
  
  P4 = paths.fill_paths(ADJ_D["M"], k=4)
  mio.save(P4, open("data/all_k61_0.5_dot_nw.adj.paths.k4.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")
  print np.sum(P4!=Pinf)
  
  P5 = paths.fill_paths(ADJ_D["M"], k=5)
  mio.save(P5, open("data/all_k61_0.5_dot_nw.adj.paths.k5.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")
  print np.sum(P5!=Pinf)

  P6 = paths.fill_paths(ADJ_D["M"], k=6)
  mio.save(P6, open("data/all_k61_0.5_dot_nw.adj.paths.k6.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")
  print np.sum(P6!=Pinf)

  P7 = paths.fill_paths(ADJ_D["M"], k=7)
  mio.save(P7, open("data/all_k61_0.5_dot_nw.adj.paths.k7.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")
  print np.sum(P7!=Pinf)

  P8 = paths.fill_paths(ADJ_D["M"], k=8)
  mio.save(P8, open("data/all_k61_0.5_dot_nw.adj.paths.k8.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")
  print np.sum(P8!=Pinf)

  P9 = paths.fill_paths(ADJ_D["M"], k=9)
  mio.save(P9, open("data/all_k61_0.5_dot_nw.adj.paths.k9.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")
  print np.sum(P9!=Pinf)

  P10 = paths.fill_paths(ADJ_D["M"], k=10)
  mio.save(P10, open("data/all_k61_0.5_dot_nw.adj.paths.k10.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")
  print np.sum(P10!=Pinf)

  P11 = paths.fill_paths(ADJ_D["M"], k=11)
  mio.save(P11, open("data/all_k61_0.5_dot_nw.adj.paths.k11.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")
  print np.sum(P11!=Pinf)

  P12 = paths.fill_paths(ADJ_D["M"], k=12)
  mio.save(P12, open("data/all_k61_0.5_dot_nw.adj.paths.k12.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")
  print np.sum(P12!=Pinf)

  P13 = paths.fill_paths(ADJ_D["M"], k=13)
  mio.save(P13, open("data/all_k61_0.5_dot_nw.adj.paths.k13.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")
  print np.sum(P13!=Pinf)

  P14 = paths.fill_paths(ADJ_D["M"], k=14)
  mio.save(P14, open("data/all_k61_0.5_dot_nw.adj.paths.k14.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")
  print np.sum(P14!=Pinf)

  P15 = paths.fill_paths(ADJ_D["M"], k=15)
  mio.save(P15, open("data/all_k61_0.5_dot_nw.adj.paths.k15.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")
  print np.sum(P15!=Pinf)

  P16 = paths.fill_paths(ADJ_D["M"], k=16)
  mio.save(P15, open("data/all_k61_0.5_dot_nw.adj.paths.k16.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")
  print np.sum(P16!=Pinf)
  # 3: load ranks
  # 4: 

if __name__ == "__main__":
  main()

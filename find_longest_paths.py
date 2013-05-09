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
  mio.save(Pinf, open("data/all_k61_0.5_dot_nw.adj.paths.k3.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")

  # 2.2: find paths k=2
  P2 = paths.fill_paths(ADJ_D["M"], k=2)
  mio.save(Pinf, open("data/all_k61_0.5_dot_nw.adj.paths.k2.csv","w"), ftype="txt", row_ids=ADJ_D['row_ids'], col_ids=ADJ_D['col_ids'], fmt="%d", delimit_c=",")

  # 3: load ranks
  ranks = load_ranks(open(RANKS_FNAME))
  print ranks


def load_ranks(fp):
  ranks = []
  for line in fp:
    line = line.strip()
    if not line: continue
    members = set(line.split(','))
    ranks.append(members)
  return ranks
    
if __name__ == "__main__":
  main()

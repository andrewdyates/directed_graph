#!/usr/bin/python
# python parse_graphviz_plain.py ~/may9_all_trans_0.6_dot_nw.dot.plain
"""
FROM
http://www.graphviz.org/doc/info/output.html#d:plain
 graph scale width height
 node name x y width height label style shape color fillcolor
 edge tail head n x1 y1 .. xn yn [label xl yl] style color
 stop
"""


import sys
fp = open(sys.argv[1])

levels = {}
for line in fp:
    line = line.strip()
    if not line: continue
    row = line.split(' ')
    if not row or row[0] != "node": continue
    name = row[1].strip('"')
    x, y = float(row[2]), float(row[3])
    if y not in levels:
        levels[y] = set([name])
    else:
        levels[y].add(name)

print >>sys.stderr, "# levels:", len(levels)
for lvl in sorted(levels):
    print >>sys.stderr, lvl
    print ",".join(sorted(levels[lvl]))

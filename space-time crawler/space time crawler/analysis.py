import csv
from numpy           import *
f = open('frontier_summary.txt', 'r')
lines = f.readlines()
d = {}
for line in lines:
    p = line.split()
    if len(p)!=2:
        continue
    d[p[0]] = p[1]
f.close()

print len(d)
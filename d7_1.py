import numpy as np

with open('inputs/d7.txt', 'r') as in_f:
    crabs = [int(x) for x in in_f.readline().split(',')]

print(sum([abs(x - int(np.median(crabs))) for x in crabs]))

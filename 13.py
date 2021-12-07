import numpy as np

with open('inputs/13.txt', 'r') as in_f:
    crabs = [int(x) for x in in_f.readline().split(',')]

print(sum([abs(x - np.mean(crabs)) for x in crabs]))

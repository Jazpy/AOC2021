import numpy as np

right = []
with open('inputs/15.txt', 'r') as in_f:
  for line in in_f:
    split = line.split('|')
    right.append([len(x) for x in split[1].split()])

count = 0
for s in right:
  for e in s:
    if e == 2 or e == 4 or e == 3 or e == 7:
      count += 1

print(count)

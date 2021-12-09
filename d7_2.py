import numpy as np

with open('inputs/d7.txt', 'r') as in_f:
    crabs = [int(x) for x in in_f.readline().split(',')]

def spend_fuel(n):
  return n * (n + 1) // 2

mid = round(np.mean(crabs))
fuels = []
for i in range(mid - 1, mid + 1):
  fuels.append(sum([spend_fuel(abs(x - i)) for x in crabs]))

print(min(fuels))

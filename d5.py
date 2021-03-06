import numpy as np
import math

with open('inputs/d5.txt', 'r') as in_f:
  lines = in_f.readlines()

coords = []
diagram = np.zeros((1000, 1000))
for line in lines:
  ps = line.strip().split('->')
  coords.append([[int(p.split(',')[0]), int(p.split(',')[1])] for p in ps])

# Silver
overlaps = 0
for (p0, p1) in coords:
  (x_0, y_0) = p0
  (x_1, y_1) = p1

  if x_0 == x_1:
    x_iter = [x_0] * (abs(y_1 - y_0) + 1)
    y_iter = range(min(y_0, y_1), max(y_0, y_1) + 1)
  elif y_0 == y_1:
    x_iter = range(min(x_0, x_1), max(x_0, x_1) + 1)
    y_iter = [y_0] * (abs(x_1 - x_0) + 1)
  else:
    continue

  for x, y in zip(x_iter, y_iter):
    if diagram[y, x] == 1:
      overlaps += 1
    diagram[y, x] += 1

print(overlaps)

# Gold
overlaps = 0
diagram = np.zeros((1000, 1000))
for (p0, p1) in coords:
  (x_0, y_0) = p0
  (x_1, y_1) = p1

  if x_0 == x_1:
    x_iter = [x_0] * (abs(y_1 - y_0) + 1)
    y_iter = range(min(y_0, y_1), max(y_0, y_1) + 1)
  elif y_0 == y_1:
    x_iter = range(min(x_0, x_1), max(x_0, x_1) + 1)
    y_iter = [y_0] * (abs(x_1 - x_0) + 1)
  else:
    x_sign = int(math.copysign(1, x_1 - x_0))
    y_sign = int(math.copysign(1, y_1 - y_0))
    x_iter = range(x_0, x_1 + x_sign, x_sign)
    y_iter = range(y_0, y_1 + y_sign, y_sign)

  for x, y in zip(x_iter, y_iter):
    if diagram[y, x] == 1:
      overlaps += 1
    diagram[y, x] += 1

print(overlaps)

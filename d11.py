import numpy as np

def invalid(o, x, y):
  return x < 0 or x >= len(o) or y < 0 or y >= len(o[0])

def flash(o, x, y, f):
  for i in range(-1, 2):
    for j in range(-1, 2):
      if invalid(o, x + i, y + j) or o[x + i, y + j] == 10:
        continue

      o[x + i, y + j] += 1

      if o[x + i, y + j] == 10:
        f.append([x + i, y + j])

flashes = 0
gold    = 0
octopi  = np.genfromtxt('inputs/d11.txt', delimiter=1, dtype=int)

while True:
  octopi += 1
  gold   += 1
  delta_flashes = 0
  flashers = np.argwhere(octopi == 10).tolist()

  while flashers:
    curr = flashers.pop()
    flash(octopi, curr[0], curr[1], flashers)
    delta_flashes += 1

  octopi %= 10

  if gold <= 100:
    flashes += delta_flashes

  if delta_flashes == 100:
    break

print(flashes)
print(gold)

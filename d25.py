import numpy as np

with open('inputs/d25.txt', 'r') as in_f:
  lines = [x.strip() for x in in_f.readlines()]

mapper = {'.': 0, '>': 1, 'v': 2}
width  = len(lines[0])
height = len(lines)

cucumbers    = np.zeros((height, width), dtype=int)
right_coords = []
down_coords  = []

for i, line in enumerate(lines):
  for j, c in enumerate(line):
    to_add = mapper[c]

    if to_add == 1:
      right_coords.append([i, j])
    elif to_add == 2:
      down_coords.append([i, j])

    cucumbers[i, j] = to_add

moved_flag   = True
iter_counter = 0
while moved_flag:
  moved_flag = False

  # Right cucumbers
  right_neighbors_coords = [[x[0], (x[1] + 1) % width] for x in right_coords]
  right_neighbors = np.array([cucumbers[x[0], x[1]] for x in right_neighbors_coords])
  zero_neighbors = np.nonzero(right_neighbors == 0)[0]
  for idx in zero_neighbors:
    cucumbers[right_coords[idx][0], right_coords[idx][1]] = 0
    cucumbers[right_neighbors_coords[idx][0], right_neighbors_coords[idx][1]] = 1
    right_coords[idx] = right_neighbors_coords[idx]

  if len(zero_neighbors) > 0:
    moved_flag = True

  # Down cucumbers
  down_neighbors_coords = [[(x[0] + 1) % height, x[1]] for x in down_coords]
  down_neighbors = np.array([cucumbers[x[0], x[1]] for x in down_neighbors_coords])
  zero_neighbors = np.nonzero(down_neighbors == 0)[0]
  for idx in zero_neighbors:
    cucumbers[down_coords[idx][0], down_coords[idx][1]] = 0
    cucumbers[down_neighbors_coords[idx][0], down_neighbors_coords[idx][1]] = 2
    down_coords[idx] = down_neighbors_coords[idx]

  if len(zero_neighbors) > 0:
    moved_flag = True

  iter_counter += 1

print(iter_counter)

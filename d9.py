import bisect

with open('inputs/d9.txt', 'r') as in_f:
  lines = [x.strip() for x in in_f.readlines()]

map = []
for line in lines:
  map.append([int(x) for x in line])

def test_low(mat, x, y, max_x, max_y):
  curr = mat[x][y]

  left = map[x - 1][y] if x != 0 else 10
  right = map[x + 1][y] if x != len(map) - 1 else 10
  up = map[x][y - 1] if y != 0 else 10
  down = map[x][y + 1] if y != len(map[0]) - 1 else 10

  if up > curr and down > curr and left > curr and right > curr:
    return curr + 1
  return 0

def color_basin(map, x, y):
  if map[x][y] == 9:
    return 0

  map[x][y] = 9

  left = color_basin(map, x - 1, y) if x != 0 else 0
  right = color_basin(map, x + 1, y) if x != len(map) - 1 else 0
  up = color_basin(map, x, y - 1) if y != 0 else 0
  down = color_basin(map, x, y + 1) if y != len(map[0]) - 1 else 0

  return 1 + left + right + up + down

# Silver
sum = 0
for x in range(len(map)):
  for y in range(len(map[0])):
    sum += test_low(map, x, y, len(map), len(map[0]))

print(sum)

# Gold
sizes = []
for x in range(len(map)):
  for y in range(len(map[0])):
    if map[x][y] != 9:
      bisect.insort(sizes, color_basin(map, x, y))

prod = 1
for x in sizes[len(sizes) - 3:]:
  prod *= x

print(prod)

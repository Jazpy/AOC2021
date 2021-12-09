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

sum = 0
for x in range(len(map)):
  for y in range(len(map[0])):
    sum += test_low(map, x, y, len(map), len(map[0]))

print(sum)

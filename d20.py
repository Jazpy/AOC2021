with open('inputs/d20.txt', 'r') as in_f:
  lines = [x.strip() for x in in_f.readlines()]

class Image:
  mapper = {'#': '1', '.': '0'}

  def __init__(self, lines):
    self.im = []
    for i, l in enumerate(lines):
      if not l:
        continue
      elif i == 0:
        self.algo = ''.join(l)
      else:
        row = [x for x in l]
        self.im.append(row)

  def smart_get(self, x, y, flip):
    if x < 0 or x >= len(self.im[0]) or y < 0 or y >= len(self.im):
      if flip and self.algo[0] == '#':
        return '#'
      else:
        return '.'
    return self.im[y][x]

  def get_surrounding(self, x, y, flip):
    ret = []
    for i in range(-1, 2):
      for j in range(-1, 2):
        ret.append(self.smart_get(x + j, y + i, flip))
    return int(''.join([Image.mapper[x] for x in ret]), 2)

  def apply(self, n):
    for a in range(n):
      new_image = []
      for i in range(-1, len(self.im) + 1):
        new_row = []
        for j in range(-1, len(self.im[0]) + 1):
          algo_coord = self.get_surrounding(j, i, a % 2 == 1)
          algo_char  = self.algo[algo_coord]
          new_row.append(algo_char)

        new_image.append(new_row)
      self.im = new_image

  def count(self):
    ret = 0
    for l in self.im:
      ret += l.count('#')
    return ret

  def print_image(self):
    for l in self.im:
      print(''.join(l))
    print('')

image = Image(lines)

# Silver
image.apply(2)
print(image.count())
# Gold
image.apply(48)
print(image.count())

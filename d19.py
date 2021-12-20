import itertools

with open('inputs/d19.txt', 'r') as in_f:
  lines = [x.strip() for x in in_f.readlines()]

class Scanner:
  class Point:
    def __init__(self, x, y, z, s=None):
      if s:
        toks = [int(t) for t in s.split(',')]
        self.x = toks[0]
        self.y = toks[1]
        self.z = toks[2]
      else:
        self.x = x
        self.y = y
        self.z = z

    def distance(self, o):
      return abs(self.x - o.x) + abs(self.y - o.y) + abs(self.z - o.z)

    def __str__(self):
      return f'({self.x}, {self.y}, {self.z})'

    def __eq__(self, o):
      return self.x == o.x and self.y == o.y and self.z == o.z

    def __hash__(self):
      return hash(self.x) ^ hash(self.y) ^ hash(self.z)

  def __init__(self, idx):
    self.id = idx
    self.loc = self.Point(0, 0, 0)
    self.points = []
    self.aligned = True if idx == 0 else False
    self.no_align = []

  def add_point(self, s):
    self.points.append(self.Point(None, None, None, s))

  def get_rotations(self, x, y, z):
    return [
      self.Point(x,y,z),self.Point(x,z,-y),self.Point(x,-y,-z),self.Point(x,-z,y),
      self.Point(-x,-y,z),self.Point(-x,z,y),self.Point(-x,y,-z),self.Point(-x,-z,-y),
      self.Point(y,-x,z),self.Point(y,z,x),self.Point(y,x,-z),self.Point(y,-z,-x),
      self.Point(-y,x,z),self.Point(-y,z,-x),self.Point(-y,-x,-z),self.Point(-y,-z,x),
      self.Point(z,y,-x),self.Point(z,-x,-y),self.Point(z,-y,x),self.Point(z,x,y),
      self.Point(-z,-y,-x),self.Point(-z,-x,y),self.Point(-z,y,x),self.Point(-z,x,-y)
    ]

  def build_rotations(self):
    self.rotations = [[] for _ in range(24)]
    for p in self.points:
      rots = self.get_rotations(p.x, p.y, p.z)
      for i, r in enumerate(rots):
        self.rotations[i].append(r)

  def get_absolute_points(self):
    ret = []
    for p in self.points:
      ret.append(self.Point(p.x + self.loc.x, p.y + self.loc.y,
                            p.z + self.loc.z))
    return ret

  def align(self, o):
    if self.id in o.no_align or o.id in self.no_align or o.aligned:
      return False

    found_align = False
    for rot in o.rotations:
      for p_ref, p_o in itertools.product(self.points, rot):
        shift = [p_ref.x - p_o.x, p_ref.y - p_o.y, p_ref.z - p_o.z]
        hits = 0
        for p in rot:
          shifted = self.Point(p.x + shift[0], p.y + shift[1], p.z + shift[2])
          if shifted in self.points:
            hits += 1
          if hits == 12:
            found_align = True
            correct_shift = shift
            break
        if found_align:
          break
      if found_align:
        break

    if found_align:
      o.loc.x = self.loc.x + correct_shift[0]
      o.loc.y = self.loc.y + correct_shift[1]
      o.loc.z = self.loc.z + correct_shift[2]
      o.points = rot
      o.aligned = True

    return found_align

# Parse input
scanners = []
for line in lines:
  if not line:
    continue
  elif 'scanner' in line:
    scanners.append(Scanner(int(line.split()[2])))
  else:
    scanners[-1].add_point(line)

for s in scanners:
  s.build_rotations()

aligned = [scanners[0]]
unaligned = scanners[1:]

while len(aligned) != len(scanners):
  new_aligned = aligned
  for s0, s1 in itertools.product(aligned, unaligned):
    if s0.align(s1):
      new_aligned.append(s1)
  aligned = new_aligned

# Puzzle outputs
silver = set()
for s in aligned:
  for p in s.get_absolute_points():
    silver.add(p)

gold = 0
for s0, s1 in itertools.product(scanners, scanners):
  dist = s0.loc.distance(s1.loc)
  if dist > gold:
    gold = dist

print(len(silver))
print(gold)

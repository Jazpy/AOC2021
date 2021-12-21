import itertools
import multiprocessing
import math

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

    def euclidean_distance(self, o):
      return math.sqrt((self.x-o.x)**2+(self.y-o.y)**2+(self.z-o.z)**2)

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

  def build_rotations_worker(s):
    return s.build_rotations()

  def build_fingerprints_worker(s):
    return s.build_fingerprints()

  def build_distance_worker(s0, s1):
    return s0.loc.distance(s1.loc)

  def build_points_worker(s):
    return s.get_absolute_points()

  def add_point(self, s):
    self.points.append(self.Point(None, None, None, s))

  def add_rotations(self, r):
    self.rotations = r

  def add_fingerprints(self, f):
    self.fingerprints = f

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
    rotations = [[] for _ in range(24)]
    for p in self.points:
      rots = self.get_rotations(p.x, p.y, p.z)
      for i, r in enumerate(rots):
        rotations[i].append(r)
    return rotations

  def build_fingerprints(self):
    fingerprints = set()
    for p0, p1 in itertools.combinations(self.points, 2):
      fingerprints.add(p0.euclidean_distance(p1))
    return fingerprints

  def get_absolute_points(self):
    return [self.Point(p.x + self.loc.x, p.y + self.loc.y, p.z + self.loc.z)
            for p in self.points]

  def single_rotation_check(self, rot_points):
    miss_check = min(len(self.points), len(rot_points)) - 12

    for p_ref, p_o in itertools.product(self.points, rot_points):
      shift = [p_ref.x - p_o.x, p_ref.y - p_o.y, p_ref.z - p_o.z]
      hits = miss = 0
      for p in rot_points:
        shifted = self.Point(p.x + shift[0], p.y + shift[1], p.z + shift[2])

        if shifted in self.points:
          hits += 1
        else:
          miss += 1

        if miss > miss_check:
          break
        elif hits == 12:
          return (True, shift, rot_points)
    return (False, 0, [])

  def align(self, o, pool):
    found_align = False
    if (o.id in self.no_align or o.aligned or
        len(self.fingerprints.intersection(o.fingerprints)) < 12):
      return found_align

    results = pool.map(self.single_rotation_check, o.rotations)

    for found, shift, rot in results:
      if found:
        found_align = True
        o.loc.x = self.loc.x + shift[0]
        o.loc.y = self.loc.y + shift[1]
        o.loc.z = self.loc.z + shift[2]
        o.points = rot
        o.aligned = True
        break

    if not found_align:
      self.no_align.append(o.id)

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

# For parallelizing various parts of the problem
pool = multiprocessing.Pool(multiprocessing.cpu_count())

# Build 24 rotations for each scanner
rotations = pool.map(Scanner.build_rotations_worker, scanners)
for s, r in zip(scanners, rotations):
  s.add_rotations(r)

# Build distances between all points inside a scanner for all scanners. This
# can be used as a fingerprinting heuristic to determine if two scaners
# will align or not.
fingerprints = pool.map(Scanner.build_fingerprints_worker, scanners)
for s, f in zip(scanners, fingerprints):
  s.add_fingerprints(f)

# Align all scanners
aligned = [scanners[0]]
unaligned = scanners[1:]

while len(aligned) != len(scanners):
  new_aligned = aligned
  for s0, s1 in itertools.product(aligned, unaligned):
    if s0.align(s1, pool):
      new_aligned.append(s1)
      unaligned.remove(s1)
  aligned = new_aligned

# Puzzle outputs
silver = set()
abs_points = pool.map(Scanner.build_points_worker, aligned)
for points in abs_points:
  for p in points:
    silver.add(p)

distances = pool.starmap(Scanner.build_distance_worker,
  [x for x in itertools.product(scanners, repeat=2)])
gold = max(distances)

print(len(silver))
print(gold)

# Done parallelizing
pool.close()
pool.join()

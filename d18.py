import math
import copy
import itertools

with open('inputs/d18.txt', 'r') as in_f:
  lines = [x.strip() for x in in_f.readlines()]

class Snail:
  # Constructor
  def __init__(self, val, left=None, right=None):
    if val is not None:
      self.is_lit = True
      self.lit    = val
    else:
      self.is_lit = False
      self.lit    = val
    self.l      = left
    self.r      = right
    self.p      = None

    if self.l:
      self.l.p = self
    if self.r:
      self.r.p = self

  # Sum definition
  def __add_neighbor(snail, val, left):
    curr_s = snail
    curr_p = curr_s.p

    while curr_p and (curr_s == curr_p.l) == left:
      curr_s = curr_p
      curr_p = curr_p.p

    if not curr_p:
      return

    curr_s = curr_p.l if left else curr_p.r

    while not curr_s.is_lit:
      curr_s = curr_s.r if left else curr_s.l

    curr_s.lit += val

  def __explode_aux(snail):
    left_v  = snail.l.lit
    right_v = snail.r.lit

    Snail.__add_neighbor(snail, left_v, True)
    Snail.__add_neighbor(snail, right_v, False)

    snail.is_lit = True
    snail.lit    = 0
    snail.l      = None
    snail.r      = None

  def explode(self, l):
    if self.is_lit:
      return False

    if l == 4:
      Snail.__explode_aux(self)
      return True

    return self.l.explode(l + 1) or self.r.explode(l + 1)

  def split(self):
    if self.is_lit and self.lit > 9:
      new_l = math.floor(self.lit / 2)
      new_r = math.ceil(self.lit / 2)

      self.is_lit = False
      self.lit    = None
      self.l      = Snail(new_l)
      self.r      = Snail(new_r)
      self.l.p    = self
      self.r.p    = self

      return True
    elif self.is_lit:
      return False

    return self.l.split() or self.r.split()

  def __add__(self, o):
    new_snail = Snail(None, self, o)

    check = True
    while check:
      check = new_snail.explode(0)
      check = check or new_snail.split()

    return new_snail

  # Magnitude
  def magnitude(self):
    if self.is_lit:
      return self.lit

    return 3 * self.l.magnitude() + 2 * self.r.magnitude()

  # I/O
  def from_string(line, i):
    curr = line[i]

    if(curr == '['):
      left, i = Snail.from_string(line, i + 1)
      right, i = Snail.from_string(line, i + 1)

      return (Snail(None, left, right), i + 1)
    else:
      return (Snail(int(curr)), i + 1)

  def __str__(self):
    if self.is_lit:
      return str(self.lit)
    return '[' + str(self.l) + ', ' + str(self.r) + ']'

snails = [Snail.from_string(line, 0)[0] for line in lines]
c_snails = copy.deepcopy(snails)

sum_snail = snails[0]
for snail in snails[1:]:
  sum_snail += snail

# Silver
print(sum_snail.magnitude())

# Gold
max_sum = 0
for x, y in itertools.product(c_snails, repeat=2):
  x0 = copy.deepcopy(x)
  y0 = copy.deepcopy(y)
  x1 = copy.deepcopy(x)
  y1 = copy.deepcopy(y)
  s0 = (x0 + y0).magnitude()
  s1 = (x1 + y1).magnitude()

  max_sum = s0 if s0 > max_sum else max_sum
  max_sum = s1 if s1 > max_sum else max_sum
print(max_sum)

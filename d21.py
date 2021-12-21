import itertools
from functools import cache

with open('inputs/d21.txt', 'r') as in_f:
  lines = [x.strip() for x in in_f.readlines()]

in_0 = int(lines[0].split()[-1])
in_1 = int(lines[1].split()[-1])

# Silver
def deterministic(p0_p, p1_p):
  p0_s = p1_s = rolls = 0

  for i in range(1, 1000, 6):
    p0_p += i + (i + 1) + (i + 2)
    rolls += 3
    if p0_p > 10:
      p0_p = 10 if p0_p % 10 == 10 else p0_p % 10
    p0_s += p0_p

    if p0_s >= 1000:
      return p1_s * rolls

    p1_p += (i + 3) + (i + 4) + (i + 5)
    rolls += 3
    if p1_p > 10:
      p1_p = 10 if p1_p % 10 == 0 else p1_p % 10
    p1_s += p1_p

    if p1_s >= 1000:
      return p0_s * rolls

print(deterministic(in_0, in_1))

# Gold
@cache
def dirac(turn, p0_score, p1_score, p0_pos, p1_pos):
  if p0_score >= 21 or p1_score >= 21:
    return (turn + 1) % 2

  ret = 0
  for x, y, z in itertools.product([1, 2, 3], repeat=3):
    new_pos = p0_pos + x + y + z if turn == 0 else p1_pos + x + y + z
    if new_pos > 10:
      new_pos = 10 if new_pos % 10 == 0 else new_pos % 10
    new_score = p0_score + new_pos if turn == 0 else p1_score + new_pos

    if turn == 0:
      ret += dirac(1, new_score, p1_score, new_pos, p1_pos)
    else:
      ret += dirac(0, p0_score, new_score, p0_pos, new_pos)

  return ret

print(dirac(0, 0, 0, in_0, in_1))

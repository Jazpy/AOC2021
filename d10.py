import bisect

with open('inputs/d10.txt', 'r') as in_f:
    lines = [x.strip() for x in in_f.readlines()]

closers = {'(': ')', '[': ']', '{': '}', '<': '>'}
points  = {')': 3, ']': 57, '}': 1197, '>': 25137}
points2 = {')': 1, ']': 2, '}': 3, '>': 4}
illegals = []
scores = []

for line in lines:
  next_closers = []
  illegal_flag = False

  # PART 1
  for c in line:
    if c in ['(', '[', '{', '<']:
      next_closers.append(closers[c])
    elif c != next_closers.pop():
      illegals.append(c)
      illegal_flag = True
      break

  if illegal_flag:
    continue

  # PART 2
  score = 0
  while next_closers:
    score = 5 * score + points2[next_closers.pop()]

  bisect.insort(scores, score)

print(sum([points[x] for x in illegals]))
print(scores[len(scores) // 2])

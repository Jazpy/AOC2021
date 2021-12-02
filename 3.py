with open('inputs/3.txt', 'r') as in_f:
  commands = in_f.readlines()
commands = [comm.split() for comm in commands]

depth = 0
horizontal = 0

for comm in commands:
  c = comm[0]
  v = int(comm[1])

  if c == 'forward':
    horizontal += v
  elif c == 'down':
    depth += v
  else:
    depth -= v

print(depth * horizontal)

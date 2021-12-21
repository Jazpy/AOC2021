with open('inputs/d3.txt', 'r') as in_f:
  numbers = [x.strip() for x in in_f.readlines()]

# Silver
gamma = 0
epsilon = 0

for i in range(len(numbers[0])):
  count = 0

  for number in numbers:
    if number[-(i + 1)] == '1':
      count += 1

  g, e = (1, 0) if count > (len(numbers) / 2) else (0, 1)
  gamma += g * (2 ** i)
  epsilon += e * (2 ** i)

print(gamma * epsilon)

# Gold
o2 = numbers
co2 = o2.copy()

def get_count(l, i):
  count = 0
  for e in l:
    if e[i] == '1':
      count += 1

  return count

for i in range(len(o2[0])):
  if len(o2) == 1 and len(co2) == 1:
    break

  if len(o2) > 1:
    c = get_count(o2, i)
    char = '1' if c >= len(o2) / 2 else '0'
    o2 = list(filter(lambda x: (x[i] == char), o2))

  if len(co2) > 1:
    c = get_count(co2, i)
    char = '0' if c >= len(co2) / 2 else '1'
    co2 = list(filter(lambda x: (x[i] == char), co2))

print(int(o2[0], 2) * int(co2[0], 2))

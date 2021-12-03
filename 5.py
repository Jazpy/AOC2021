with open('inputs/5.txt', 'r') as in_f:
  numbers = [x.strip() for x in in_f.readlines()]

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

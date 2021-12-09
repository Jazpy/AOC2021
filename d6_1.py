lanternfish = [0] * 9

with open('inputs/d6.txt', 'r') as in_f:
    start = [int(x) for x in in_f.readline().split(',')]

for s in start:
    lanternfish[s] += 1

iters = 80

for _ in range(iters):
    spawners = lanternfish[0]
    for j in range(len(lanternfish) - 1):
        lanternfish[j] = lanternfish[j + 1]
    lanternfish[6] += spawners
    lanternfish[8]  = spawners

print(sum(lanternfish))

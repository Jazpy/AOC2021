with open('inputs/d1.txt', 'r') as in_f:
  reads = in_f.readlines()

reads = [int(read) for read in reads]

past = reads[0]
count = 0

for read in reads[1:]:
  if read > past:
    count += 1

  past = read

print(count)

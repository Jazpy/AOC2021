with open('inputs/d1.txt', 'r') as in_f:
  reads = in_f.readlines()

reads = [int(read) for read in reads]

past = reads[0] + reads[1] + reads[2]
count = 0

for i in range(1, len(reads) - 2):
  curr_window = past + reads[i + 2] - reads[i - 1]

  if curr_window > past:
    count += 1

  past = curr_window

print(count)

import numpy as np

right = []
left  = []
with open('inputs/15.txt', 'r') as in_f:
  for line in in_f:
    split = line.split('|')
    left.append([x for x in split[0].split()])
    right.append([x for x in split[1].split()])

class Display:
  def __init__(self, left, right):
    self.decoder = self.create_decoder(left)
    self.num     = self.decode(right)

  def intersect(self, s0, s1):
    return len(set(s0).intersection(set(s1)))

  def create_decoder(self, l):
    decoder = [''] * 10

    # Easy numbers first
    for s in l:
      if len(s) == 2:
        decoder[1] = ''.join(sorted(s))
      elif len(s) == 4:
        decoder[4] = ''.join(sorted(s))
      elif len(s) == 3:
        decoder[7] = ''.join(sorted(s))
      elif len(s) == 7:
        decoder[8] = ''.join(sorted(s))

    # Harder numbers now
    for s in l:
      shared = self.intersect(s, decoder[1])

      # 2, 3, or 5
      if len(s) == 5:
        if shared == 2:
          decoder[3] = ''.join(sorted(s))
        else:
          shared = self.intersect(s, decoder[4])
          if shared == 2:
            decoder[2] = ''.join(sorted(s))
          else:
            decoder[5] = ''.join(sorted(s))
      # 0, 5, or 9
      elif len(s) == 6:
        if shared == 1:
          decoder[6] = ''.join(sorted(s))
        else:
          shared = self.intersect(s, decoder[4])
          if shared == 4:
            decoder[9] = ''.join(sorted(s))
          else:
            decoder[0] = ''.join(sorted(s))

    return decoder

  def decode(self, r):
    tens = 1000
    ret  = 0
    for s in r:
      ret += tens * self.decoder.index(''.join(sorted(s)))
      tens //= 10

    return ret

  def get_num(self):
    return self.num

final_sum = 0
for l, r in zip(left, right):
  final_sum += Display(l, r).get_num()

print(final_sum)

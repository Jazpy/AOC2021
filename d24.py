class ALU:
  def __init__(self, n):
    self.digits = [int(x) for x in n]

  def smart_z(self):
    s_z = self.digits[0] + 15
    s_z = s_z * 26 + self.digits[1] + 8
    s_z = s_z * 26 + self.digits[2] + 2

    # d2 - 7 = d3
    if (s_z % 26) - 9 == self.digits[3]:
      s_z = s_z // 26
    else:
      s_z = s_z // 26
      s_z = s_z * 26 + self.digits[3] + 6

    s_z = s_z * 26 + self.digits[4] + 13
    s_z = s_z * 26 + self.digits[5] + 4
    s_z = s_z * 26 + self.digits[6] + 1

    # d6 - 4 = d7
    if (s_z % 26) - 5 == self.digits[7]:
      s_z = s_z // 26
    else:
      s_z = s_z // 26
      s_z = s_z * 26 + self.digits[7] + 9

    s_z = s_z * 26 + self.digits[8] + 5

    # d8 - 2 = d9
    if (s_z % 26) - 7 == self.digits[9]:
      s_z = s_z // 26
    else:
      s_z = s_z // 26
      s_z = s_z * 26 + self.digits[9] + 13

    # d5 - 8 = d10
    if (s_z % 26) - 12 == self.digits[10]:
      s_z = s_z // 26
    else:
      s_z = s_z // 26
      s_z = s_z * 26 + self.digits[10] + 9

    # d4 + 3 = d11
    if (s_z % 26) - 10 == self.digits[11]:
      s_z = s_z // 26
    else:
      s_z = s_z // 26
      s_z = s_z * 26 + self.digits[11] + 6

    # d1 + 7 = d12
    if (s_z % 26) - 1 == self.digits[12]:
      s_z = s_z // 26
    else:
      s_z = s_z // 26
      s_z = s_z * 26 + self.digits[12] + 2

    # d0 + 4 = d13
    if (s_z % 26) - 11 == self.digits[13]:
      s_z = s_z // 26
    else:
      s_z = s_z // 26
      s_z = s_z * 26 + self.digits[13] + 2

    return s_z

print(ALU(str(52926995971999)).smart_z())
print(ALU(str(11811951311485)).smart_z())

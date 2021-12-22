with open('inputs/d22.txt', 'r') as in_f:
  lines = [x.strip() for x in in_f.readlines()]

class Cube:
  def __init__(self, on, x_min, x_max, y_min, y_max, z_min, z_max, l=None):
    if l is not None:
      self.on = l.split()[0] == 'on'
      toks = l.split()[1].split(',')
      self.x_min = int(toks[0].split('=')[1].split('..')[0])
      self.x_max = int(toks[0].split('=')[1].split('..')[1])
      self.y_min = int(toks[1].split('=')[1].split('..')[0])
      self.y_max = int(toks[1].split('=')[1].split('..')[1])
      self.z_min = int(toks[2].split('=')[1].split('..')[0])
      self.z_max = int(toks[2].split('=')[1].split('..')[1])
    else:
      self.on = on
      self.x_min = x_min
      self.x_max = x_max
      self.y_min = y_min
      self.y_max = y_max
      self.z_min = z_min
      self.z_max = z_max

    self.e_x = (self.x_max - self.x_min) / 2
    self.e_y = (self.y_max - self.y_min) / 2
    self.e_z = (self.z_max - self.z_min) / 2
    self.c_x = self.x_min + self.e_x
    self.c_y = self.y_min + self.e_y
    self.c_z = self.z_min + self.e_z

  def is_big(self):
    return (self.x_min < -50 or self.x_max > 50 or
            self.y_min < -50 or self.y_max > 50 or
            self.z_min < -50 or self.z_max > 50)

  def volume(self):
    x_len = self.x_max - self.x_min + 1
    y_len = self.y_max - self.y_min + 1
    z_len = self.z_max - self.z_min + 1
    return x_len * y_len * z_len

  def intersects(self, o):
    if (abs(self.c_x - o.c_x)-(self.e_x+o.e_x) <= 0 and
        abs(self.c_y - o.c_y)-(self.e_y+o.e_y) <= 0 and
        abs(self.c_z - o.c_z)-(self.e_z+o.e_z) <= 0):
       return True
    return False

  def contains(self, o):
    if (self.x_min >= o.x_min and self.x_max <= o.x_max and
        self.y_min >= o.y_min and self.y_max <= o.y_max and
        self.z_min >= o.z_min and self.z_max <= o.z_max):
      return self
    elif (o.x_min >= self.x_min and o.x_max <= self.x_max and
          o.y_min >= self.y_min and o.y_max <= self.y_max and
          o.z_min >= self.z_min and o.z_max <= self.z_max):
      return o
    return None

  def split(self, o):
    splits = []
    i_x_min = max(self.x_min, o.x_min)
    i_x_max = min(self.x_max, o.x_max)
    i_y_min = max(self.y_min, o.y_min)
    i_y_max = min(self.y_max, o.y_max)
    i_z_min = max(self.z_min, o.z_min)
    i_z_max = min(self.z_max, o.z_max)

    # X from left
    if self.x_min < i_x_min:
      splits.append(Cube(self.on, self.x_min, i_x_min - 1,
                         self.y_min, self.y_max, self.z_min, self.z_max))
      self.x_min = i_x_min
    # And right
    if i_x_max < self.x_max:
      splits.append(Cube(self.on, i_x_max + 1, self.x_max,
                         self.y_min, self.y_max, self.z_min, self.z_max))
      self.x_max = i_x_max
    # Y from below
    if self.y_min < i_y_min:
      splits.append(Cube(self.on, self.x_min, self.x_max,
                         self.y_min, i_y_min - 1, self.z_min, self.z_max))
      self.y_min = i_y_min
    # And above
    if i_y_max < self.y_max:
      splits.append(Cube(self.on, self.x_min, self.x_max,
                         i_y_max + 1, self.y_max, self.z_min, self.z_max))
      self.y_max = i_y_max
    # Z from behind
    if self.z_min < i_z_min:
      splits.append(Cube(self.on, self.x_min, self.x_max,
                         self.y_min, self.y_max, self.z_min, i_z_min - 1))
      self.z_min = i_z_min
    # And front
    if i_z_max < self.z_max:
      splits.append(Cube(self.on, self.x_min, self.x_max,
                         self.y_min, self.y_max, i_z_max + 1, self.z_max))
      self.z_max = i_z_max

    return splits

# Solve as we parse
silver_flag = True
cubes = [Cube(None, None, None, None, None, None, None, lines[0])]
for line in lines[1:]:
  new_cube = Cube(None, None, None, None, None, None, None, line)

  # Output silver when we start reading bigger cubes
  if silver_flag and new_cube.is_big():
    print(sum([x.volume() for x in cubes]))
    silver_flag = False

  new_cubes = []

  add_flag = new_cube.on
  for i, cube in enumerate(cubes):
    # No intersection
    if not cube.intersects(new_cube):
      new_cubes.append(cube)
      continue

    contained = cube.contains(new_cube)
    # Old cube in list is contained, do not add to new cubes
    if contained and contained == cube:
      continue
    # New cube is contained, add the container and rest of list unchanged
    if contained and contained == new_cube:
      if new_cube.on:
        new_cubes += cubes[i:]
        add_flag = False
        break
    # Else, we have to split (also if contained and off)
    splits = cube.split(new_cube)
    new_cubes += splits

  if add_flag:
    new_cubes.append(new_cube)

  cubes = new_cubes

# Gold
print(sum([x.volume() for x in cubes]))

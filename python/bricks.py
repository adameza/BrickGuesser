class SimpleCube(object):

    def __init__(self, x, y, z):
      self.x = x
      self.y = y
      self.z = z
      self.prefix = "1 0 "
      self.postfix = " 1 0 0 0 1 0 0 0 1 p\\box.dat\n"

    def __str__(self):
      return f"({self.x}, {self.y}, {self.z})"

    def writeToFile(self, file):
      # check if brick already exists
      for line in file:
        if line == self.__makeString:
          return

      print(f"Writing simple cube with coordinates ({self.x},  {self.y},  {self.z})")
      file.write(self.__makeString())

    def __makeString(self):
      coord = str(self.x) + " " + str(self.y) + " " + str(self.z)
      return self.prefix + coord + self.postfix

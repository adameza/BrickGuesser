class SimpleCube(object):

    def __init__(self, x, y, z):
      self.x = x
      self.y = y
      self.z = z
      self.prefix = "1 0 "
      self.postfix = " 1 0 0 0 1 0 0 0 1 p\\box.dat\n"

    def __str__(self):
      return f"({self.x}, {self.y}, {self.z})"

    def __eq__(self, other):
        """Overrides the default implementation"""
        if other.x == self.x and other.y == self.y and other.z == self.z:
          return True
        else:
          return False

    def writeToFile(self, file):
      # print(f"Writing simple cube with coordinates ({self.x},  {self.y},  {self.z})")
      file.write(self.__makeString())

    def __makeString(self):
      coord = str(self.x) + " " + str(self.y) + " " + str(self.z)
      return self.prefix + coord + self.postfix

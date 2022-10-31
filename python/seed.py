import random

class Seed(object):
  
  def __init__(self):
    self.shapesChoices = ["cube", "pyramid", "sphere"]
    self.shape = "default"
    self.xOffsets = []
    self.yOffsets = []
    self.height = 0
    self.width = 0
    self.length = 0
    self.radius = 0
    self.numShapes = 0

  def genSize(self):
    match self.shape:
      case "cube":
        self.width = random.randrange(10, 50, 1)
        self.length = random.randrange(10, 50, 1)
        self.height = random.randrange(10, 50, 1)
      case "pyramid":
        self.width = random.randrange(7, 50, 1)
        self.length = self.width
        self.height = random.randrange(6, self.width, 1)
      case "sphere":
        self.width = random.randrange(9, 50, 1)
        self.length = self.width

  def genOffsets(self):
    # spacing = random.randrange(0, 6, 2)
    spacing = 4
    self.xOffsets.append(0) # shape 0 gets offsetx 0
    self.yOffsets.append(0) # shape 0 gets offsety 0
    match self.numShapes:
      case 2:
        self.xOffsets.append(2 * (self.length) + spacing)
        self.yOffsets.append(0)

      case 3:
        self.xOffsets.append(2 * (self.length) + spacing)
        self.yOffsets.append(0)

        self.xOffsets.append((self.length) + spacing)
        self.yOffsets.append(2 * (self.width) + spacing)

      case 4:
        self.xOffsets.append(2 * (self.length) + spacing)
        self.yOffsets.append(0)

        self.xOffsets.append(0)
        self.yOffsets.append(2 * (self.width) + spacing)

        self.xOffsets.append(2 * (self.length) + spacing)
        self.yOffsets.append(2 * (self.width) + spacing)

      case 5:
        self.xOffsets.append(2 * (self.length) + spacing)
        self.yOffsets.append((self.width) + spacing)

        self.xOffsets.append(2 * (self.length) + spacing)
        self.yOffsets.append(-1*((self.width) + spacing))

        self.xOffsets.append(-1*(2 * (self.length) + spacing))
        self.yOffsets.append((self.width) + spacing)

        self.xOffsets.append(-1*(2 * (self.length) + spacing))
        self.yOffsets.append(-1*((self.width) + spacing))

  def generate(self):
    # get a random shape
    self.shape = random.choice(self.shapesChoices)
    # generate a random size for that shape
    self.genSize()
    # generate a number of shapes
    # self.numShapes = random.randrange(1, 5, 1)
    self.numShapes = 4
    # generate offsets
    self.genOffsets()
    #roof or ceiling for pyramid/sphere


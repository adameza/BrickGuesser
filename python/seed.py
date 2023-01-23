""" 
Random events that can give a unqie structure

-Initial Shape (cube, sphere, pyramid)
-Size of shapes
-Number of shapes
-Floor
-Ceiling
-Pillars
  -height and width

 """

import random

class Seed(object):
  
  def __init__(self, zOffset, maxWidth):
    self.shapesChoices = ["sphere", "pyramid", "cube"]
    self.shape = "default"
    self.xOffsets = []
    self.yOffsets = []
    self.height = 0
    self.width = 0
    self.length = 0
    self.radius = 0
    self.numShapes = 0
    self.zOffset = zOffset
    self.ceiling = 0
    self.maxWidth = maxWidth

  def genSize(self):
    match self.shape:
      case "cube":
        self.width = random.randrange(2, 15, 1)
        self.length = random.randrange(1, 15, 1)
        self.height = random.randrange(1, 15, 1)
      case "pyramid":
        self.width = random.randrange(1, 15, 1)
        self.length = self.width
        self.height = random.randrange(0, self.width, 1)
      case "sphere":
        self.width = random.randrange(2, 15, 1)
        self.length = self.width
        self.height = self.width

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

  def calc_ceiling(self):
    if self.shape == 'pyramid':
      realheight = (self.width // 2)
      if (self.height > realheight):
        self.ceiling = realheight
      else:
        self.ceiling = self.height
      self.ceiling = ((self.ceiling-1)*2)+2 + self.zOffset
    elif self.shape == "cube":
      self.ceiling = (self.height*2) + self.zOffset
    elif self.shape == "sphere":
      self.ceiling = (self.width-4) + self.zOffset

  def generate(self):
    # get a random shape
    self.shape = random.choice(self.shapesChoices)
    # generate a random size for that shape
    self.genSize()
    # generate a number of shapes
    self.numShapes = random.randrange(3, 5, 1)
    # generate offsets
    self.genOffsets()
    self.calc_ceiling()
    #floor or ceiling for pyramid/sphere
    # if self.shape is "pyramid" or self.shape is "sphere":
    #   self.genFloorCeiling()


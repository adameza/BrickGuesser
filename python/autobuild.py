#!/usr/bin/env python3
import bricks as bricks
import seed as seed
import random

title_line = "0 Name: Test\n"


class autobuilder(object):

  def __init__(self, fileName):
    self.fileName = fileName
    self.numLevels = 1

  def readSimpleCube(self, line):
    """ Takes a line from .ldr file and converts to object """
    postIndex = line.index(" 0 0 0 1 0 0 0 1 p\\box.dat")
    coord = line[4:postIndex+1].split(" ")
    # print(f"block = ({int(coord[0])}, {int(coord[1])}, {int(coord[2])}\n")
    return bricks.SimpleCube(int(coord[0]), int(coord[1]), int(coord[2]))

  def verifyFile(self, file, allCubes):
    # Read in the file once and build a list of line offsets
    blank = []
    line_offset = []
    offset = 0
    for line in file:
        line_offset.append(offset)
        offset += len(line)
    file.seek(0)

    for index in range(0, len(allCubes)):
      for i in range(0, index):
        if allCubes[i] == allCubes[index]:
          file.seek(line_offset[i])
          file.write(blank)
          return False
    return True

  def getBlocks(self, file):
    """ Takes a file and converts all the lines into
        a list of objects """
    boxes = []
    for line in file.readlines():
      if line.find("1 0 0 0 1 0 0 0 1 p\\box.dat") > 0:
        boxes.append(self.readSimpleCube(line))
    return boxes

  def writeCeiling(self, file, offset_x, offset_y, offset_z):
    print(f"args ({offset_x}, {offset_y}, {offset_z})\n")
    for x in range(offset_x):
      for y in range(offset_y):
        myCube = bricks.SimpleCube((x * 2), offset_z, (y * 2))
        myCube.writeToFile(file)

  def writeRectangle(self, file, cols, rows, height, offset_x, offset_y, offset_z):
    if random.randrange(0, 10) > 5:
      cols = cols // 2
    for z in range (0, height):
      for x in range (0, rows):
        for y in range(0, cols):
          # coordinates are a little weird on ldcad (x, z, y)... z being height
          myCube = bricks.SimpleCube((x * 2)+offset_x, (z*2) + offset_z, (y * 2)+offset_y)
          myCube.writeToFile(file)

  def writePyramid(self, file, width, height, offset_x, offset_y, offset_z):
    if random.randrange(0, 10) > 5:
      width = random.randrange(width, width*2)
    for z in range (0, height):
      for x in range (0, width - z*2):
        for y in range(0, width - z*2):
          # coordinates are a little weird on ldcad (x, z, y)... z being height
          myCube = bricks.SimpleCube((x * 2)+offset_x+z*2, (z*2) + offset_z, (y * 2)+offset_y+z*2)
          myCube.writeToFile(file)

  def writeSphere(self, file, radius, offset_x, offset_y, offset_z):
    if random.randrange(0, 10) > 5:
      radius = random.randrange(radius, radius*2)
    for z in range (0, radius):
      for x in range (0, (radius-4) - z*2):
        for y in range(0, (radius-4) - z*2):
          # coordinates are a little weird on ldcad (x, z, y)... z being height
          upside = bricks.SimpleCube((x * 2)+offset_x+z*2, (z*2) + offset_z, (y * 2)+offset_y+z*2)
          upside.writeToFile(file)
    for z in range (1, radius):
      for x in range (0, (radius-4) - z*2):
        for y in range(0, (radius-4) - z*2):
          # coordinates are a little weird on ldcad (x, z, y)... z being height
          downside = bricks.SimpleCube((x * 2)+offset_x+z*2, -(z*2) + offset_z, (y * 2)+offset_y+z*2)
          downside.writeToFile(file)

  def run(self, f, seed):
    for index in range(0, seed.numShapes):
      if seed.shape == "pyramid":
        self.writePyramid(f, seed.width, seed.height, seed.xOffsets[index], seed.yOffsets[index], seed.zOffset)
      if seed.shape == "sphere":
        self.writeSphere(f, seed.width, seed.xOffsets[index], seed.yOffsets[index], seed.zOffset)
      if seed.shape == "cube":
        self.writeRectangle(f, seed.width, seed.length, seed.height, seed.xOffsets[index], seed.yOffsets[index], seed.zOffset)
    # write ceiling, not sure why minus 2 on offsets, but it is needed
    if seed.shape == "cube":
      self.writeCeiling(f, seed.xOffsets[1]-2, seed.yOffsets[2]-2, seed.ceiling)
    if seed.shape == "pyramid":
      self.writeCeiling(f, seed.xOffsets[1]-2, seed.yOffsets[2]-2, seed.ceiling)
    if seed.shape == "sphere":
      self.writeCeiling(f, seed.xOffsets[1]-2, seed.yOffsets[2]-2, seed.ceiling)

def main():
  mySim = autobuilder('../ldraw/testStruct.ldr')
  # mySeed = seed.Seed(0)
  with open(mySim.fileName, 'w') as f:
    f.close()

  print(f"Opening {mySim.fileName} ...", end =" ")
  with open(mySim.fileName, 'r+') as f:
    print("Success")

    numLevels = random.randrange(4, 12, 1)
    levels = [None] * numLevels
    maxWidth = 50
    for i in range(numLevels):
      if i == 0:
        levels[i] = seed.Seed(0, 50)
        levels[i].generate()
        maxWidth = levels[i].width

      else:
        levels[i] = seed.Seed(levels[i-1].ceiling + 2, maxWidth)
      levels[i].generate()
      mySim.run(f, levels[i])

    #remove duplicates in testStruct.ldr and write to output.ldr
    seen = set()
    print("Removing duplicates in output file")
    with open('../ldraw/testStruct.ldr', 'r') as fin, open('../ldraw/output.ldr', 'w') as fout:
        for line in fin:
            h = hash(line)
            if h not in seen:
                fout.write(line)
                seen.add(h)

    print("File closed. Exiting...")

  # print(f"w {mySeed.width}, h {mySeed.height}\n")

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()

""" 
w 34, h 28 -> 16
w 30, h 8  -> 7
w 14, h 10 -> 6
w 34, h 22 -> 16
w 39, h 36 -> 18
w 47, h 34 -> 23
w 12, h 10 -> 5
 """
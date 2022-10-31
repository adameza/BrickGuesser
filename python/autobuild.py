#!/usr/bin/env python3
import bricks as bricks
import seed as seed
import random

title_line = "0 Name: Test\n"


class autobuilder(object):

  def __init__(self, fileName):
    self.fileName = fileName

  def readSimpleCube(self, line):
    """ Takes a line from .ldr file and converts to object """
    postIndex = line.index(" 0 0 0 1 0 0 0 1 p\\box.dat")
    coord = line[4:postIndex+1].split(" ")
    return bricks.SimpleCube(int(coord[0]), int(coord[1]), int(coord[2]))

  # deprecated
  # def getBlocks(file):
  #   """ Takes a file and converts all the lines into
  #       a list of objects """
  #   boxes = []
  #   for line in file.readlines():
  #     if line.find(" p\\box.dat") > 0:
  #       boxes.append(readBox(line))
  #   return boxes

  def writeRectangle(self, file, cols, rows, height, offset_x, offset_y):
    for z in range (0, height):
      for x in range (0, rows):
        for y in range(0, cols):
          # coordinates are a little weird on ldcad (x, z, y)... z being height
          myCube = bricks.SimpleCube((x * 2)+offset_x, (z*2), (y * 2)+offset_y)
          myCube.writeToFile(file)

  def writePyramid(self, file, width, height, offset_x, offset_y):
    for z in range (0, height):
      for x in range (0, width - z*2):
        for y in range(0, width - z*2):
          # coordinates are a little weird on ldcad (x, z, y)... z being height
          myCube = bricks.SimpleCube((x * 2)+offset_x+z*2, (z*2), (y * 2)+offset_y+z*2)
          myCube.writeToFile(file)

  def writeSphere(self, file, radius, offset_x, offset_y):
    for z in range (0, radius):
      for x in range (0, (radius-4) - z*2):
        for y in range(0, (radius-4) - z*2):
          # coordinates are a little weird on ldcad (x, z, y)... z being height
          upside = bricks.SimpleCube((x * 2)+offset_x+z*2, (z*2), (y * 2)+offset_y+z*2)
          upside.writeToFile(file)
    for z in range (1, radius):
      for x in range (0, (radius-4) - z*2):
        for y in range(0, (radius-4) - z*2):
          # coordinates are a little weird on ldcad (x, z, y)... z being height
          downside = bricks.SimpleCube((x * 2)+offset_x+z*2, -(z*2), (y * 2)+offset_y+z*2)
          downside.writeToFile(file)

  def run(self, seed):
      print(f"Opening {self.fileName} ...", end =" ")
      with open(self.fileName, 'w') as f:
        print("Success")
        # Read the current file contents
        # print("Fetching boxes from file contents...")
        # boxes = getBlocks(f)
        # for box in boxes:
        #   print(box)
        # self.writeRectangle(f, 3, 3, 2, 0, 10)
        # self.writePyramid(f, 8, 5, 18, 0)
        # self.writePyramid(f, 8, 5, 0, 0)
        # self.writePyramid(f, 8, 5, 9, 18)
        # self.writeSphere(f, 9, 25, 25)
        for index in range(0, seed.numShapes):
          if seed.shape == "pyramid":
            self.writePyramid(f, seed.width, seed.height, seed.xOffsets[index], seed.yOffsets[index])
          if seed.shape == "sphere":
            self.writeSphere(f, seed.width, seed.xOffsets[index], seed.yOffsets[index])
          if seed.shape == "cube":
            self.writeRectangle(f, seed.width, seed.length, seed.height, seed.xOffsets[index], seed.yOffsets[index])
        f.close
      print("File closed. Exiting...")

def main():
  mySim = autobuilder('../ldraw/testStruct.ldr')
  mySeed = seed.Seed()
  mySeed.generate()
  mySim.run(mySeed)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
#!/usr/bin/env python3
import module
import random

title_line = "0 Name: Test\n"


def readBox(line):
  """ Takes a line from .ldr file and converts to object """
  postIndex = line.index(" 0 0 0 1 0 0 0 1 p\\box.dat")
  coord = line[4:postIndex+1].split(" ")
  return module.box(int(coord[0]), int(coord[1]), int(coord[2]))

def getBlocks(file):
  """ Takes a file and converts all the lines into
      a list of objects """
  boxes = []
  for line in file.readlines():
    if line.find(" p\\box.dat") > 0:
      boxes.append(readBox(line))
  return boxes

def writePlane(file, cols, rows, height, offset_x, offset_y):
  numblocks = cols * rows
  colsCount = 0
  for i in range (0, cols):
    newBox = module.box(0+offset_x, 0, (i * 2)+offset_y)
    newBox.writeToFile(file)
    for j in range (0, rows):
      rowBox = module.box(0+offset_x, j*2, i*2)
      rowBox.writeToFile(file)
      for z in range(0, height):
        zBox = module.box((z * 2)+offset_x, j * 2, (i * 2)+offset_y)
        zBox.writeToFile(file)

def main():
    """ Main entry point of the app """
    myBox = module.box(1, 2, 3)
    print("Opening ldraw/testStruct.ldr ...", end =" ")
    with open('../ldraw/testStruct.ldr', 'w') as f:
      print("Success")
      # Read the current file contents
      # print("Fetching boxes from file contents...")
      # boxes = getBlocks(f)
      # for box in boxes:
      #   print(box)
      writePlane(f, 3, 20, 3, 0, 0)
      writePlane(f, 3, 20, 3, 10, 0)
      f.close
    print("File closed. Exiting...")



if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
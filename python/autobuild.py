#!/usr/bin/env python3
import module

def makeBox(line):
  """ Takes a line from .ldr file and converts to object """
  postIndex = line.index(" 1 0 0 0 1 0 0 0 1 p\\box.dat")
  coord = line[3:postIndex+1].split(" ")
  return module.box(int(coord[0]), int(coord[1]), int(coord[2]))

def getBlocks(file):
  """ Takes a file and converts all the lines into
      a list of objects """
  boxes = []
  for line in file.readlines():
    if line.find(" p\\box.dat") > 0:
      boxes.append(makeBox(line))
  return boxes

def main():
    """ Main entry point of the app """
    myBox = module.box(1, 2, 3)
    print("Opening ldraw/testStruct.ldr ...", end =" ")
    with open('../ldraw/testStruct.ldr', 'r') as f:
      print("Success")
      # Read the current file contents
      print("Fetching boxes from file contents...")
      boxes = getBlocks(f)
      for box in boxes:
        print(box)
      f.close
    print("File closed. Exiting...")



if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
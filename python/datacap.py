import pyautogui
import time
from autobuild import *
from seed import *
import os
# print(pyautogui.size())

# scripts button (294, 51)
  # samples button (396, 210)
  # camera test (345, 329)
  # stop playback (1134, 1085)
  # start playback (1236, 1085) have 4 seconds 
  # pause playback (1078, 1090)

# file = (28,52)
  # export button = (73, 413)
  
# opengl export = (155,186)

# path input = (990, 663)

#ctrl+a
# delete

#type path

# final export button (680, 705)

# final ok (1141,652)

# pyautogui.displayMousePosition()

# "ok" for in between builds (757,723)
totalBuilds = 100
pics_per_build = 3

def main():
  for build_num in range(totalBuilds):
    
    mySim = autobuilder('../ldraw/testStruct.ldr')
    # clear whatever is currently in the file
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
          levels[i] = seed.Seed(0, 10)
          levels[i].generate()
          maxWidth = levels[i].width

        else:
          levels[i] = seed.Seed(levels[i-1].ceiling + 2, maxWidth)
        levels[i].generate()
        mySim.run(f, levels[i])
      mySim.deleteRandomBricks()
      #remove duplicates in testStruct.ldr and write to output.ldr
      seen = set()
      print("Removing duplicates in output file")
      lineCount = 0
      with open('../ldraw/testStruct.ldr', 'r') as fin, open('../ldraw/output.ldr', 'w') as fout:
          for line in fin:
              h = hash(line)
              if h not in seen:
                  fout.write(line)
                  lineCount+=1
                  seen.add(h)

      print("File closed. Exiting...")
      
      
    for pic_num in range(pics_per_build):
        
        
      # render time
      time.sleep(1)
        
      #first make sure on correct workspace
      pyautogui.hotkey("win", "4")
      time.sleep(0.1)
      
      # pass thourhg file change prompt
      pyautogui.click(757, 723)
      time.sleep(0.1)
      
      if pic_num == 0:
        folder = "build_" + str(build_num)
        path = "/home/adam/Poly/SeniorProject/generated_data/" + folder
        os.mkdir(path)
        
        #refresh screen
        # click file botton
        pyautogui.moveTo(28, 52)
        pyautogui.click(28, 52)
        time.sleep(0.1)
        
        pyautogui.moveTo(59, 189)
        pyautogui.click(59, 189)
        time.sleep(0.1)
      
      #rotate object
      pyautogui.moveTo(365, 1066)
      x_change = 365 + random.randrange(5, 150)
      y_change = 1066 + random.randrange(-150, -5)
      pyautogui.dragTo(x_change, y_change, button='left', duration=0.5)
      time.sleep(0.1)
      
      # click file botton
      pyautogui.moveTo(28, 52)
      pyautogui.click(28, 52)
      time.sleep(0.1)
      
      # click export button
      pyautogui.click(73, 413)
      time.sleep(0.1)
      
      # click opengl
      pyautogui.click(155,186)
      time.sleep(0.1)
      
      # click path input box and clear contents
      pyautogui.click(990,663)
      pyautogui.hotkey("ctrl", "a")
      pyautogui.hotkey("backspace")
      time.sleep(0.1)
      
      # type path
      name = "/build_" + str(build_num) + "_pic" + str(pic_num) + "_" + str(lineCount) + ".png"
      pyautogui.typewrite(path + name)
      time.sleep(0.1)
      
      # final export button
      pyautogui.click(680,705)
      time.sleep(0.5)
      
      # click ok button
      pyautogui.click(1141,652)
      time.sleep(0.1)
  
if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
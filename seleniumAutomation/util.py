import pyautogui

def keydownAndPress(keydown:str , press:str):
  pyautogui.keyDown(keydown)
  pyautogui.press(press)
  pyautogui.keyUp(keydown)
  return
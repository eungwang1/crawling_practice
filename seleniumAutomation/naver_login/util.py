import pyautogui
import os


def keydownAndPress(keydown: str, press: str):
    pyautogui.keyDown(keydown)
    pyautogui.press(press)
    pyautogui.keyUp(keydown)
    return


def createDirectory(directory):
    try:
        if not os.path.isdir(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

import os
import hmac
import hashlib
from time import gmtime, strftime
import pyautogui


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


def generateHmac(method, url, secretKey, accessKey):
    path, *query = url.split("?")
    datetimeGMT = strftime('%y%m%d', gmtime()) + 'T' + \
        strftime('%H%M%S', gmtime()) + 'Z'
    message = datetimeGMT + method + path + (query[0] if query else "")

    signature = hmac.new(bytes(secretKey, "utf-8"),
                         message.encode("utf-8"),
                         hashlib.sha256).hexdigest()

    return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(accessKey, datetimeGMT, signature)

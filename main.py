#!/usr/bin/env python3
from pathlib import Path
import time
import subprocess

from hid import HIDException
import com

debug = True


def close(self: com.device):
    self.send(com.device.MSG_TYPE_FN, 0x00)


keyboard = com.device(0x32AC, 0x0012, onClose=close, debug=debug)
numpad = com.device(0x32AC, 0x0013, onClose=close, debug=debug)
backlight_path = Path("/sys/class/backlight/")
while [x for x in backlight_path.iterdir() if x.is_dir()].__len__() == 0:
    time.sleep(0.1)
backlightDevice = [x for x in backlight_path.iterdir() if x.is_dir()][0]
lastBrightness = None
command = ""


def readScreenBrightness():
    return int((backlightDevice / "brightness").read_text()) * 255 // 62194


lastBrightnessUpdate = time.time()

def handleNonRepeat(datatype, data):
    global command
    match datatype:
        case com.device.MSG_TYPE_CMD:
            command += data[1::].split(b"\x00", 1)[0].decode()
            if 0x00 in data:
                print(f"command complete: {command}")
                subprocess.Popen(command, shell=True)
                command = ""
            else:
                print(f"command partial: {command}")



while True:
    try:
        print("\033[32mConnecting...\033[0m")
        keyboard.open()
        numpad.open()
        while True:
            numpadData = numpad.read()
            keyboardData = keyboard.read()
            if numpadData:
                datatype = numpadData[0]
                if (
                    datatype >= com.device.MSG_REPEAT_START
                    and datatype <= com.device.MSG_REPEAT_END
                ):
                    keyboard.send(datatype, numpadData[1::])
                else:
                    handleNonRepeat(datatype, numpadData)

            if keyboardData:
                datatype = keyboardData[0]
                if (
                    datatype >= com.device.MSG_REPEAT_START
                    and datatype <= com.device.MSG_REPEAT_END
                ):
                    numpad.send(datatype, keyboardData[1::])
                else:
                    handleNonRepeat(datatype, keyboardData)

            brightness = readScreenBrightness()
            if brightness != lastBrightness or time.time() - lastBrightnessUpdate > 100:
                print("updating brightness")
                lastBrightnessUpdate = time.time()
                print(f"brightness: {brightness}")
                keyboard.send(com.device.MSG_TYPE_SET_BRIGHTNESS, brightness)
                numpad.send(com.device.MSG_TYPE_SET_BRIGHTNESS, brightness)
                lastBrightness = brightness
            time.sleep(0.01)
    except (HIDException, IOError) as e:
        print("\033[31mNot connected", e, "\033[0m")
        keyboard.close()
        numpad.close()
        print("\033[31mClosed devices\033[0m")
        time.sleep(1)
        print(f"\033[31m{e}\033[0m")
    except KeyboardInterrupt:
        keyboard.close()
        numpad.close()

        exit(0)

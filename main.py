#!/usr/bin/env python3
from pathlib import Path
import time

from hid import HIDException
import com
debug = True
def close(self:com.device):
    self.send(com.device.MSG_TYPE_FN_RECV,0x00)
keyboard = com.device(0x32ac, 0x0012,onClose=close,debug=debug)
numpad = com.device(0x32ac, 0x0013,  onClose=close,debug=debug)
def readScreenBrightness():
    backlight_path = Path("/sys/class/backlight/amdgpu_bl2")
    return int((backlight_path / "brightness").read_text())*255//62194
    
lastBrightnessUpdate = time.time()
    
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
                match datatype:
                    case com.device.MSG_TYPE_FN_SEND:
                        keyboard.send(com.device.MSG_TYPE_FN_RECV,numpadData[1])
                    case com.device.MSG_TYPE_DC_SEND:
                        keyboard.send(com.device.MSG_TYPE_DC_RECV,numpadData[1])
                    case com.device.MSG_TYPE_XM_SEND:
                        keyboard.send(com.device.MSG_TYPE_XM_RECV,numpadData[1])
                    case com.device.MSG_TYPE_CMD:
                        print(numpadData[1::].decode())
            
            if keyboardData:
                datatype = keyboardData[0]
                match datatype:
                    case com.device.MSG_TYPE_FN_SEND:
                        numpad.send(com.device.MSG_TYPE_FN_RECV,keyboardData[1])
            if time.time()-lastBrightnessUpdate > 1:
                print("updating brightness")
                lastBrightnessUpdate = time.time()
                brightness = readScreenBrightness()
                print(f"brightness: {brightness}")
                keyboard.send(com.device.MSG_TYPE_SET_BRIGHTNESS,brightness)
                numpad.send(com.device.MSG_TYPE_SET_BRIGHTNESS,brightness)
            time.sleep(0.01)
    except (HIDException, IOError) as e:
        print("\033[31mNot connected",e,"\033[0m")
        keyboard.close()
        numpad.close()
        print("\033[31mClosed devices\033[0m")
        time.sleep(1)
        print(f"\033[31m{e}\033[0m")
    except KeyboardInterrupt:
        keyboard.close()
        numpad.close()
        exit(0)
        
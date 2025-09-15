import board, digitalio, usb_hid, json

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard import Keycode
from adafruit_hid.mouse import Mouse

class KeyboardPico():
    def __init__(self, keyFile = "./config/keyconfig.json"):
        self.redLED = digitalio.DigitalInOut(board.GP25)
        self.redLED.direction = digitalio.Direction.OUTPUT

        self.keyconfigFile = keyFile
        self.keyboard = Keyboard(usb_hid.devices)
        self.mouse    = Mouse(usb_hid.devices)
        with open(self.keyconfigFile, "r", encoding = "UTF-8") as keyDataFile:
            self.keyconfig = json.loads(keyDataFile.read())
            
        for p in self.keyconfig["key"].keys():
            exec(f"{p} = digitalio.DigitalInOut(board.{p})")
            exec(f"{p}.switch_to_input(pull=digitalio.Pull.DOWN)")
            exec(f"{p}Val = 0")
            exec(f"{p}Back = 0")
        
        while True:
            self.redLED.value = False
            for p, k in self.keyconfig["key"].items():
                exec(f"{p}Val = {p}.value")
                if eval(f"{p}Val == 1") and eval(f"{p}Back == 0"):
                    keyList=[]
                    for kc in k:
                        keyList.append(eval(kc))
                    self.keyboard.send(*keyList)
                    print(k)
                    self.redLED.value = True
                exec(f"{p}Back = {p}Val")



if __name__ == "__main__":
    KeyboardPico()
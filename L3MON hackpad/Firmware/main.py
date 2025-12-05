import board
import busio

from kmk.extensions.display import Oled
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.scanners.encoder import RotaryioEncoder
from kmk.modules.macros import Press, Release, Tap, Macros

class MyKeyboard(KMKKeyboard):
    def __init__(self):
        super().__init__()

        # create and register the scanner
        self.matrix = RotaryioEncoder(
            pin_a=board.GP0,
            pin_b=board.GP1,
            # optional
            divisor=4,
        )
        
keyboard = KMKKeyboard()

i2c = busio.I2C(board.GP6, board.GP7)

macros = Macros()
keyboard.modules.append(macros)


oled = Oled(
    width=128, height=32, i2c=busio.I2C(board.GP6, board.GP7)
)

def oled_callback(oled):
    oled.clear()
    oled.text(f'Batt: {battery}%', 0, 0)
    oled.text(f'Vol: {volume}%', 0, 10)
    oled.show()

PINS = [board.D3, board.D4, board.D2, board.D1]

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)


keyboard.keymap = [
    [KC.A, KC.DELETE, KC.MACRO("Hello world!"), KC.Macro(Press(KC.LCMD), Tap(KC.S), Release(KC.LCMD)),]
]

# Start kmk!
if __name__ == '__main__':
    keyboard.go()
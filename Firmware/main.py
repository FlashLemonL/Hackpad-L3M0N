import board
import busio

from kmk.extensions.display import Oled
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.scanners.encoder import RotaryioEncoder
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.encoder import EncoderHandler
        
keyboard = KMKKeyboard()

i2c = busio.I2C(board.GP6, board.GP7)

encoder_handler = EncoderHandler()
macros = Macros()
keyboard.modules.appenf(encoder_handler)
keyboard.modules.append(macros)
keyboard.extensions.append(MediaKeys())

oled = Oled(
    width=128, height=32, i2c=busio.I2C(board.GP6, board.GP7)
)

def oled_callback(oled):
    oled.clear()
    oled.text(f'Batt: {battery}%', 0, 0)
    oled.text(f'Vol: {volume}%', 0, 10)
    oled.show()

oled.set_callback(oled_callback)
keyboard.extensions.append(oled)

PINS = [board.GP28, board.GP0, board.GP1, board.GP2, board.GP4, board.GP3]
encoder_handler.pins=[(board.GP27, board.GP26)]

keyboard.matrix = [
    KeysScanner(
        pins=PINS,
        value_when_pressed=False,
    )
]
encoder_handler.map=[
    [
        KC.MACRO(Press(KC.LALT), Tap(KC.TAB), Tap(KC.LEFT), Tap(KC.LEFT), Release(KC.LALT)), KC.MACRO(Press(KC.LALT), Tap(KC.TAB), Tap(KC.RIGHT), Release(KC.LALT))
    ]
]
codemode=KC.MACRO(Tap(KC.LWIN), "Github", Tap(KC.ENTER), Tap(KC.LWIN), "Visual Studio Code", Tap(KC.ENTER))
gamemode=KC.MACRO(Tap(KC.LWIN), "Opera", Tap(KC.ENTER), Tap(KC.LWIN), "Steam", Tap(KC.ENTER), Tap(KC.LWIN), "Epic Games Launcher", Tap(KC.ENTER))
keyboard.keymap = [
    [codemode, KC.V, KC.B, KC.N, KC.M, gamemode]
]

import usb_cdc
serial = usb_cdc.data

def handle_host_commands():
    if serial.in_waiting > 0:
        data = serial.readline().decode().strip()
        if data.startswith("BATT:"):
            global battery
            battery = int(data.split(":")[1])
        elif data.startswith("VOL:"):
            global volume
            volume = int(data.split(":")[1])

# Start kmk!
if __name__ == '__main__':
    while True:
        handle_host_commands()
        keyboard.go()
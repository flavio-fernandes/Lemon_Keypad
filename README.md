# Lemon_Keypad

#### CircuitPython QT_Py_RP2040 project for Adafruit Lemon Mechanical Keypad

This repo is a snapshot of all libraries and python scripts
needed to have the lemon keypad working on CircuitPython 7.x

![Lemon Keypad](https://live.staticflickr.com/65535/51731342597_fa5dab6650.jpg)

Pictures of my lemonade making [available here](https://flic.kr/s/aHBqjzvAvG)

For more info on what this project is doing, check out these learning guides from
Adafruit:

- [Lemon Mechanical Keypad](https://learn.adafruit.com/qtpy-lemon-mechanical-keypad-macropad/code)
- [CircuitPython LED Animations](https://learn.adafruit.com/circuitpython-led-animations)
- [Make It a Keyboard](https://learn.adafruit.com/make-it-a-keyboard)
- [Keypad and Matrix Scanning in CircuitPython](https://learn.adafruit.com/key-pad-matrix-scanning-in-circuitpython)
- [Customizing USB Devices in CircuitPython](https://learn.adafruit.com/customizing-usb-devices-in-circuitpython)

For a quick start on Adafruit QT Py RP2040, look at this awesome page:

- [Adafruit QT Py RP2040](https://learn.adafruit.com/adafruit-qt-py-2040)

Lastly, visit these links for a good reference on Circuit Python:

- [CircuitPython Libraries](https://learn.adafruit.com/circuitpython-essentials/circuitpython-libraries)
- [adafruit_hid](https://circuitpython.readthedocs.io/projects/hid/en/latest/)
- [adafruit_led_animation](https://circuitpython.readthedocs.io/projects/led-animation/en/latest/)
- [keypad](https://circuitpython.readthedocs.io/en/latest/shared-bindings/keypad/)

### Changing CIRCUITPY version

Download CircuitPython [.UF2 file for QT Py RP2040](https://circuitpython.org/board/adafruit_qtpy_rp2040/).
Reboot into bootloader mode and drag the .UF2 file into the `RPI-RP2` drive.

```
# NOTE: Do not do this before backing up all files!!!
>>> import microcontroller as mc ; mc.on_next_reset(mc.RunMode.UF2) ; mc.reset()
```

:warning: **Important:** This project has a [`boot.py`](https://github.com/flavio-fernandes/Lemon_Keypad/blob/main/boot.py) file that will normally skip initializing
the storage, midi, and serial peripherals. In order to change this behavior, simply hold down
any of the keypads right after plugging the device to an USB port. 

### Removing _all_ files from CIRCUITPY drive

```
# NOTE: Do not do this before backing up all files!!!
>>> import storage ; storage.erase_filesystem()
```

### Copying files from cloned repo to CIRCUITPY drive
```
# First, get to the REPL prompt so the board will not auto-restart as
# you copy files into it

# Assuming that QTPy is mounted under /Volumes/CIRCUITPY
$  cd ${THIS_REPO_DIR}
$  [ -d /Volumes/CIRCUITPY/ ] && \
   rm -rf /Volumes/CIRCUITPY/* && \
   (tar czf - *) | ( cd /Volumes/CIRCUITPY ; tar xzvf - ) && \
   echo ok || echo not_okay
```

## A little more info about the code

Once properly started, the lemon will be recognized as a keyboard.
Upon releasing all keys, a value between 1 and 62 will be generated, depending
on what keys were pressed.
The value will be surrounded by a hard-coded prefix and suffix.
Feel free to change that! In my day-to-day usage, I map the generated string
into a command via [textExpander](https://textexpander.com/).

```text
;#@lime1#
;#@lime2#
;#@lime3#
;#@lime4#
...
;#@lime8#
...
;#@lime16#
...
;#@lime32#
...
;#@lime62##
```

### Fidget mode

Hold down all keys to toggle fidget mode on/off. While in this mode, no keyboard
output takes place.

### Color animations

Press and hold any of the keypads for 3 seconds to select a neopixel animation.
Press and hold more than one keypad to turn animations off.


 

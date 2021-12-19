import time
import board
import keypad
import usb_hid
import neopixel
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation import color
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# When all buttons are released, this code will type the mask of what
# had been pressed, surrounded by the prefix and suffix below.
MSG_PREFIX = ";#@lime"
MSG_SUFFIX = "#"

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

# This is the pin in the board that is connected to the NeoPixel Jewel - 7 RGB LED
pixel_pin = board.A0
num_pixels = 7
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.8, auto_write=False)
internal_pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=1, auto_write=False)

# The button pins we'll use. Each is directly connected to a Kailh Mechanical Key Switch
buttonpins = (board.A3, board.A2, board.A1, board.D10, board.D9, board.D8)

keys = keypad.Keys(buttonpins, value_when_pressed=False, pull=True)

animation_push_button = AnimationGroup(
    Blink(pixels, speed=0.05, color=color.WHITE),
    Blink(internal_pixel, speed=0.05, color=color.WHITE),
)

animation_fidget_push_button = AnimationGroup(
    Blink(pixels, speed=0.05, color=color.PURPLE),
    Solid(internal_pixel, color=color.PURPLE),
)

animation_long_push_button = AnimationGroup(
    Blink(pixels, speed=0.05, color=color.RED),
    Solid(internal_pixel, color=color.RED),
)

animation_off = AnimationGroup(
    Solid(pixels, color=color.BLACK),
    Solid(internal_pixel, color=color.BLACK),
)

animation_groups = [
    AnimationGroup(
        Pulse(pixels, speed=0.05, color=color.ORANGE, period=10),
        Solid(internal_pixel, color=color.AMBER),
    ),
    AnimationGroup(
        Rainbow(pixels, speed=0.1, period=10),
        Solid(internal_pixel, color=color.BLACK),
    ),
    AnimationGroup(
        RainbowSparkle(pixels, speed=0.1, num_sparkles=2),
        RainbowSparkle(internal_pixel, speed=0.1, num_sparkles=0),
    ),
    AnimationGroup(
        Blink(pixels, speed=3, color=color.GOLD),
        Solid(internal_pixel, color=color.GOLD),
    ),
    AnimationGroup(
        Chase(pixels, speed=0.1, size=3, spacing=6, color=color.GREEN),
        Solid(internal_pixel, color=color.GREEN),
    ),
    AnimationGroup(
        ColorCycle(
            pixels,
            10,
            colors=[
                color.BLUE,
                color.GREEN,
                color.RED,
                color.TEAL,
                color.PURPLE,
                color.AQUA,
            ],
        ),
        Solid(internal_pixel, color=color.BLUE),
    ),
    animation_off,  # Expected to be the last one
]

# Initial animation to show that code is ready to go
start_ts = time.monotonic()
start_amin = ColorCycle(
    pixels, 0.25, colors=[color.MAGENTA, color.ORANGE, color.TEAL, color.AQUA]
)
while time.monotonic() - start_ts < 1.5:
    start_amin.animate()

ALL_BUTTONS_MASK = 2 ** len(buttonpins) - 1

# The state of the lemon keyboard
fidget_mode = False
curr_animation_group_index = -1
animations = animation_off
buttons_pressed_ts = None
buttons_pressed = 0
buttons_mask = 0
buttons_first_press = None
long_press = False

# Create an event we will reuse over and over.
event = keypad.Event()

print("Waiting for button presses")
while True:
    animations.animate()
    time.sleep(0.01)

    # Detect long press
    if (
        (not long_press)
        and buttons_pressed
        and time.monotonic() - buttons_pressed_ts > 2.8
    ):
        print("long press")
        long_press = True
        animations.reset()
        animations = animation_long_push_button

    if keys.events.get_into(event):
        pressed_mask = 2 ** event.key_number
        prev_buttons_pressed = buttons_pressed
        prev_buttons_mask = buttons_mask

        if event.pressed:
            buttons_pressed |= pressed_mask
            buttons_mask |= pressed_mask
        else:
            buttons_pressed &= ~pressed_mask

        print(
            "button",
            event.key_number,
            "pressed." if event.pressed else "released.",
            "buttons_pressed_mask:",
            buttons_pressed,
            "buttons_mask_mask:",
            buttons_mask,
            "pressed_mask:",
            pressed_mask,
        )

        if not prev_buttons_pressed and buttons_pressed:
            print("first detected press")
            # first button pressed
            animations.reset()
            animations = (
                animation_fidget_push_button if fidget_mode else animation_push_button
            )
            buttons_pressed_ts = time.monotonic()
            buttons_first_press = event.key_number
        elif prev_buttons_pressed and not buttons_pressed:
            print("last button release")
            # last button released
            if long_press:
                if buttons_mask != 2 ** buttons_first_press:
                    # long press when multiple buttons were pressed: animation off
                    curr_animation_group_index = -1
                else:
                    curr_animation_group_index = buttons_first_press % len(
                        animation_groups
                    )
            else:
                msg = f"{MSG_PREFIX}{buttons_mask}{MSG_SUFFIX}"
                if buttons_mask == ALL_BUTTONS_MASK:
                    fidget_mode = not fidget_mode
                    print("fidget mode is now", "on" if fidget_mode else "off")
                elif fidget_mode:
                    print("fidget mode message: ", msg)
                else:
                    print("typing", msg)
                    layout.write(msg)
                    time.sleep(0.3)
                    keys.events.clear()  # Empty the event queue.
            animations.reset()
            animations = animation_groups[curr_animation_group_index]
            long_press = False
            buttons_mask = 0

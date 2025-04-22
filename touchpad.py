import sys
import asyncio

import evdev
import uinput


if len(sys.argv) >= 2:
    target_device = sys.argv[1]
else:
    target_device = "/dev/input/event21"


class X:
    def __init__(self, min, max):
        self.min = min
        self.max = max


class Y:
    def __init__(self, min, max):
        self.min = min
        self.max = max


class Area:
    def __init__(self, x_min: int, x_max: int, y_min: int, y_max: int, ratio: float | None = None, touchpad=True):
        self.X = X(x_min, x_max)
        self.Y = Y(y_min, y_max)
        self.ratio = ratio if ratio else (self.X.max / self.Y.max)  # this may be inaccurate since the min values might not be 0
        self.touchpad = touchpad

    def __repr__(self) -> str:
        return f"X: {self.X.min}-{self.X.max}, Y: {self.Y.min}-{self.Y.max}, touchpad: {self.touchpad}"


def range_converter(number: int | float, old_range: int | float, new_range: int | float) -> float:
    return (number/new_range) * old_range

def convert_mouse_to_display(original_min, original_max, new_min, new_max):
    return lambda position: round(new_min + (
    (position - original_min) * (new_max - new_min)
) / (original_max - original_min))

### original ###
# in mm
width = 115
height = 77

x_min = 0
y_min = 0
x_max = 1337
y_max = 876
ratio = 1.52625570776255707763
touchpad = Area(x_min, x_max, y_min, y_max, ratio=ratio)  # object representation
### end of original ###

touchpad = Area(
    x_min + 150,
    x_max - 150,
    y_min + 100,
    y_max - 100,
    ratio=ratio
)

dx_min = 0
dy_min = 0
dx_max = 1440
dy_max = 960
d_ratio = 1.5

display = Area(dx_min, dx_max, dy_min, dy_max, ratio=d_ratio, touchpad=False)

x_offset = -50
y_offset = 0

dx_offset = 0
dy_offset = 0

def mm_to_points(axis):
    return axis

x_converter = convert_mouse_to_display(touchpad.X.min, touchpad.X.max, display.Y.min, display.Y.max)
y_converter = convert_mouse_to_display(touchpad.Y.min, touchpad.Y.max, display.X.min, display.X.max)

abs_info_x = (touchpad.X.min, touchpad.X.max, 0, 0)
abs_info_y = (touchpad.Y.min, touchpad.Y.max, 0, 0)
pressure_info = (0, 2, 0, 0)
tilt_info = (-64, 63, 0, 0)

device_info = [
    uinput.ABS_X + abs_info_x,
    uinput.ABS_Y + abs_info_y, 
    uinput.BTN_LEFT, 
    uinput.ABS_PRESSURE + pressure_info,
    uinput.ABS_TILT_X + tilt_info,
    uinput.ABS_TILT_Y + tilt_info,
    uinput.BTN_RIGHT,
    uinput.BTN_MIDDLE,
    #uinput.BTN_TOOL_DOUBLETAP,
    #uinput.BTN_TOOL_TRIPLETAP,
    # These are to emulate the tablet (no difference)
    #uinput.BTN_TOOL_PEN,
    #uinput.BTN_TOOL_RUBBER,
    #uinput.BTN_TOUCH,
    #uinput.BTN_STYLUS,
    #uinput.BTN_STYLUS2,
]

device = evdev.InputDevice(target_device)
device.grab()

try:
    with uinput.Device(device_info, name="Touchpad Tablet") as virtual_device:

        async def read_event_loop():
            async for event in device.async_read_loop():
                if event.type == 3:
                    if event.code == 0:  # ABS_X
                        await x(event.value)
                        #print("ABS_X:", event.value)
                    if event.code == 1:  # ABS_Y
                        await y(event.value)
                        #print("ABS_Y:", event.value)
                elif event.type == 1:
                    if event.code == 272:  # BTN_LEFT
                        await left(event.value)
                        await pressure(event.value)

                    if event.code == 333:  # BTN_TOOL_DOUBLETAP
                        await right(event.value)

                    if event.code == 334:  # BTN_TOOL_TRIPLETAP
                        await middle(event.value)

        async def x(value):
            virtual_device.emit(uinput.ABS_X, value + x_offset)
            #print(f"x {value + x_offset}")

        async def y(value):
            virtual_device.emit(uinput.ABS_Y, value + y_offset)
            #print(f"y {value + y_offset}")

        async def left(value):
            virtual_device.emit(uinput.BTN_LEFT, value)
            #print(f"left {value}")
            
        async def pressure(value):
            virtual_device.emit(uinput.ABS_PRESSURE, value)
            #print(f"pressure {value}")

        async def right(value):
            virtual_device.emit(uinput.BTN_RIGHT, value)
            #virtual_device.emit(uinput.BTN_TOOL_DOUBLETAP, value)

        async def middle(value):
            virtual_device.emit(uinput.BTN_MIDDLE, value)
            #virtual_device.emit(uinput.BTN_TOOL_TRIPLETAP, value)

        asyncio.run(read_event_loop())

except KeyboardInterrupt:
    print("Exited")
finally:
    device.ungrab()

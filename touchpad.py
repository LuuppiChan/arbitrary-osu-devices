import sys
import asyncio

import evdev
import uinput

def range_converter(number: int | float, old_range: int | float, new_range: int | float) -> float:
    return (number/new_range) * old_range

def convert_mouse_to_display(original_min, original_max, new_min, new_max):
    return lambda position: round(new_min + (
    (position - original_min) * (new_max - new_min)
) / (original_max - original_min))

### original ###
x_min = 0
y_min = 0
x_max = 1337
y_max = 876
### end of original ###

x_min = x_min + 150
y_min = y_min + 50
x_max = x_max - 150
y_max = y_max - 50

dx_min = 0
dy_min = 0
dx_max = 1440
dy_max = 960

x_offset = -100
y_offset = 0

dx_offset = 0
dy_offset = 0

x_converter = convert_mouse_to_display(x_min, x_max, dx_min, dx_max)
y_converter = convert_mouse_to_display(y_min, y_max, dx_min, dy_max)

abs_info_x = (x_min, x_max, 0, 0)
abs_info_y = (y_min, y_max, 0, 0)
pressure_info = (0, 2, 0, 0)
tilt_info = (-64, 63, 0, 0)

device_info = [
    uinput.ABS_X + abs_info_x,
    uinput.ABS_Y + abs_info_y, 
    uinput.BTN_LEFT, 
    uinput.ABS_PRESSURE + pressure_info,
    uinput.ABS_TILT_X + tilt_info,
    uinput.ABS_TILT_Y + tilt_info,
]

device = evdev.InputDevice(sys.argv[1])
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

        asyncio.run(read_event_loop())

except KeyboardInterrupt:
    print("Exited")
finally:
    device.ungrab()

import sys
import asyncio

import evdev
import uinput

device = evdev.InputDevice(sys.argv[1])

with uinput.Device([uinput.KEY_S]) as virtual_device:

    async def read_event_loop():
        async for event in device.async_read_loop():
            if event.type == 1:
                if event.code == 116:
                    await action(event.value)

    async def action(value):
        virtual_device.emit(uinput.KEY_S, value)
        print(f"Powerbutton event value: {value}")

    asyncio.run(read_event_loop())

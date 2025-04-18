# Arbitrary devices For osu!
Random scripts to make some device usable for osu!.

THESE ARE NOT MEANT FOR NORMAL USAGE!

These are meant for adapting into your system.

# Info about the scripts
## lid.py
- OS: Linux
- Dependencies: [python-evdev](https://github.com/gvalkov/python-evdev), [python-uinput](https://github.com/pyinput/python-uinput)
- Task: Makes my Framework 13 laptop lid switch an `s` key.
- Usage: `sudo python lid.py [/path/to/lid/switch/event]`
- Example: `sudo python lid.py /dev/input/event0`

## touchpad.py
- OS: Linux
- Dependencies: [python-evdev](https://github.com/gvalkov/python-evdev), [python-uinput](https://github.com/pyinput/python-uinput)
- Task: Makes my Framework 13 laptop touchpad a tablet-like device.
- Usage: `sudo python touchpad.py [/path/to/touchpad/event]`
- Example: `sudo python touchpad.py /dev/input/event0`

## powerbutton.py
- OS: Linux
- Dependencies: [python-evdev](https://github.com/gvalkov/python-evdev), [python-uinput](https://github.com/pyinput/python-uinput)
- Task: Makes my Framework 13 laptop powerbutton an `s` key.
- Usage: `sudo python powerbutton.py [/path/to/power/button/event]`
- Example: `sudo python powerbutton.py /dev/input/event0`

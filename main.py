from tkinter import *
from kasa import SmartStrip
from kasa import SmartPlug
import asyncio

root = Tk()

# All the lights and sockets in my house
bedroom_light = SmartPlug("192.168.1.64")
mirror_light = SmartPlug("192.168.1.65")
vanity_light = SmartPlug("192.168.1.66")
bathroom_light = SmartPlug("192.168.1.67")
asyncio.run(bedroom_light.update())
asyncio.run(mirror_light.update())
asyncio.run(vanity_light.update())
asyncio.run(bathroom_light.update())

# Turn on the light
def lightOn(light_switch):
    asyncio.run(light_switch.update())
    asyncio.run(light_switch.turn_on())
    print(light_switch.alias + " on")

# Turn off the light
def lightOff(light_switch):
    asyncio.run(light_switch.update())
    asyncio.run(light_switch.turn_off())
    print(light_switch.alias + " off")

cur_row = 0
Label(root, text=mirror_light.alias).grid(row=cur_row, column=0)
Button(root, text="on", command=lambda: lightOn(mirror_light), fg="green").grid(row=cur_row, column=1)
Button(root, text="off", command=lambda: lightOff(mirror_light), fg="red").grid(row=cur_row, column=2)
cur_row += 1

Label(root, text=bathroom_light.alias).grid(row=cur_row, column=0)
Button(root, text="on", command=lambda: lightOn(bathroom_light), fg="green").grid(row=cur_row, column=1)
Button(root, text="off", command=lambda: lightOff(bathroom_light), fg="red").grid(row=cur_row, column=2)
cur_row += 1

root.mainloop()

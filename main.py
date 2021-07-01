from tkinter import *
from kasa import SmartStrip
from kasa import SmartPlug
import asyncio
from functools import partial

root = Tk()

# The ip addresses of all the light switches
light_ip_addresses = [
    "192.168.1.64",
    "192.168.1.65",
    "192.168.1.66",
    "192.168.1.67",
    "192.168.1.70",
    "192.168.1.71",
    "192.168.1.72",
    "192.168.1.73",
    "192.168.1.74",
]

# Initialize all the light switch objects
light_switches = []

for light_ip in light_ip_addresses:
    light_switch = SmartPlug(light_ip)
    asyncio.run(light_switch.update())
    print(f"{light_switch.alias} is on: {light_switch.is_on}")
    light_switches.append(light_switch)


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


# Create the UI
cur_row = 0
for light in light_switches:
    Label(root, text=light.alias).grid(row=cur_row, column=0)
    Button(root, text="on", command=partial(lightOn, light), fg="green").grid(row=cur_row, column=1)
    Button(root, text="off", command=partial(lightOff, light), fg="red").grid(row=cur_row, column=2)
    cur_row += 1

root.mainloop()

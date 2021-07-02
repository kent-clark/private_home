#!/usr/bin/python

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
    light_switches.append(light_switch)


switch_buttons = {}
# Toggle the light
def toggle(switch):
    asyncio.run(switch.update())
    button = switch_buttons[switch]

    if switch.is_off:
        asyncio.run(switch.turn_on())
        print(f"{switch.alias} is turned on")
        button.config(fg="green")
    else:
        asyncio.run(switch.turn_off())
        print(f"{switch.alias} is turned off")
        button.config(fg="red")


# Create the UI
cur_row = 0
for light_switch in light_switches:
    toggle_button = Button(
        root,
        text=light_switch.alias,
        command=partial(toggle, light_switch),
        fg=("green" if light_switch.is_on else "red"),
        padx = 15,
        pady = 15,
    )
    switch_buttons[light_switch] = toggle_button
    toggle_button.grid(row=cur_row, column=0, sticky='nesw')
    cur_row += 1

# Make all buttons auto resize
for i in range(len(light_ip_addresses)):
    Grid.rowconfigure(root, i, weight=1)
Grid.columnconfigure(root, 0, weight=1)


if __name__=="__main__":
    root.mainloop()

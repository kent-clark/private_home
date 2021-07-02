#!/usr/bin/python

from tkinter import *
from kasa import SmartStrip
from kasa import SmartPlug
from functools import partial
import asyncio

# The ip addresses of the plugs
plug_ip_addresses = [
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

# The ip addresses of the strips
strip_ip_addresses = [
    "192.168.1.68",
]

root_window = Tk()
plug_buttons = {}


def toggle(device, plug):
    asyncio.run(device.update())
    button = plug_buttons[plug]

    if plug.is_off:
        asyncio.run(plug.turn_on())
        button.config(fg="green")
    else:
        asyncio.run(plug.turn_off())
        button.config(fg="red")


def initUI():
    cur_row = 0

    # Create buttons for plugs
    for plug_ip in plug_ip_addresses:
        smart_plug = SmartPlug(plug_ip)
        asyncio.run(smart_plug.update())
    
        toggle_button = Button(
            root_window,
            text=smart_plug.alias,
            command=partial(toggle, smart_plug, smart_plug),
            fg=("green" if smart_plug.is_on else "red"),
            padx = 50,
            pady = 30,
        )
        plug_buttons[smart_plug] = toggle_button
        toggle_button.grid(row=cur_row, column=0, sticky='nesw')
        cur_row += 1

    # Create buttons for strips
    for strip_ip in strip_ip_addresses:
        smart_strip = SmartStrip(strip_ip)
        asyncio.run(smart_strip.update())

        for plug in smart_strip.children:
            toggle_button = Button(
                root_window,
                text=plug.alias,
                command=partial(toggle, smart_strip, plug),
                fg=("green" if plug.is_on else "red"),
                padx = 50,
                pady = 30,
            )
            plug_buttons[plug] = toggle_button
            toggle_button.grid(row=cur_row, column=0, sticky='nesw')
            cur_row += 1

    # Make all buttons auto resize
    for i in range(cur_row):
        Grid.rowconfigure(root_window, i, weight=1)
    Grid.columnconfigure(root_window, 0, weight=1)

    # Config the window
    root_window.title("Private Home")
    root_window.eval('tk::PlaceWindow . center')


if __name__=="__main__":
    initUI()
    root_window.mainloop()


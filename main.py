# Color constants
red = [1, 0, 0, 1]
green = [0, 1, 0, 1]

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
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


# A list of all the smart devices
devices = []
# A mapping of the buttons to the plugs
button_plug = {}
# A mapping of the led buttons to the plugs
led_button_plug = {}


# Toggle a plug
def toggle(device, button):
    asyncio.run(device.update())
    plug = button_plug[button]

    if plug.is_on:
        asyncio.run(plug.turn_off())
        button.color = red
    else:
        asyncio.run(plug.turn_on())
        button.color = green

# Toggle a plug's led
def toggle_led(device, button):
    asyncio.run(device.update())
    plug = led_button_plug[button]

    if plug.led:
        asyncio.run(plug.set_led(False))
        button.color = red
    else:
        asyncio.run(plug.set_led(True))
        button.color = green


def refresh(delta_time):
    for device in devices:
        asyncio.run(device.update())
    for button, plug in button_plug.items():
        button.color = green if plug.is_on else red
    for led_button, plug in led_button_plug.items():
        led_button.color = green if plug.led else red


class RootGrid(GridLayout):
    def __init__(self, **kwargs):
        super(RootGrid, self).__init__(**kwargs)
        self.cols = 2

        # Create buttons for plugs and their leds
        for plug_ip in plug_ip_addresses:
            smart_plug = SmartPlug(plug_ip)
            devices.append(smart_plug)
            asyncio.run(smart_plug.update())

            toggle_button = Button(
                text=smart_plug.alias,
                color = green if smart_plug.is_on else red,
            )
            toggle_button.bind(on_press=partial(toggle, smart_plug))
            button_plug[toggle_button] = smart_plug
            self.add_widget(toggle_button)

            toggle_led_button = Button(
                text='LED',
                color = green if smart_plug.led else red,
            )
            toggle_led_button.bind(on_press=partial(toggle_led, smart_plug))
            led_button_plug[toggle_led_button] = smart_plug
            self.add_widget(toggle_led_button)

        # Create buttons for strips
        for strip_ip in strip_ip_addresses:
            smart_strip = SmartStrip(strip_ip)
            devices.append(smart_strip)
            asyncio.run(smart_strip.update())

            for plug in smart_strip.children:
                toggle_button = Button(
                    text=plug.alias,
                    color = green if plug.is_on else red,
                )
                toggle_button.bind(on_press=partial(toggle, smart_strip))
                button_plug[toggle_button] = plug
                self.add_widget(toggle_button)

        # Start the refresh clock
        Clock.schedule_interval(refresh, 5)
                

class XHomeApp(App):
    def build(self):
        return RootGrid()

if __name__ == "__main__":
    XHomeApp().run()

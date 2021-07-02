from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
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


# Color constants
red = [1, 0, 0, 1]
green = [0, 1, 0, 1]


# Toggle a plug on a device, and update the button color
def toggle(plug, device, button):
    asyncio.run(device.update())

    if plug.is_off:
        asyncio.run(plug.turn_on())
        button.color = green
    else:
        asyncio.run(plug.turn_off())
        button.color = red


class RootGrid(GridLayout):
    def __init__(self, **kwargs):
        super(RootGrid, self).__init__(**kwargs)
        self.cols = 1

        # Create buttons for plugs
        for plug_ip in plug_ip_addresses:
            smart_plug = SmartPlug(plug_ip)
            asyncio.run(smart_plug.update())
        
            toggle_button = Button(
                text=smart_plug.alias,
                color = green if smart_plug.is_on else red,
            )
            toggle_button.bind(on_press=partial(toggle, smart_plug, smart_plug))
            self.add_widget(toggle_button)

        # Create buttons for strips
        for strip_ip in strip_ip_addresses:
            smart_strip = SmartStrip(strip_ip)
            asyncio.run(smart_strip.update())

            for plug in smart_strip.children:
                toggle_button = Button(
                    text=plug.alias,
                    color = green if plug.is_on else red,
                )
                toggle_button.bind(on_press=partial(toggle, plug, smart_strip))
                self.add_widget(toggle_button)
                

class PrivateHomeApp(App):
    def build(self):
        return RootGrid()

if __name__ == "__main__":
    PrivateHomeApp().run()

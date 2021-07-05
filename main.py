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
from threading import Thread
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

def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()

loop = asyncio.new_event_loop()
Thread(target=start_background_loop, args=(loop,), daemon=True).start()


async def toggle_async(device, button):
    plug = button_plug[button]

    button.disabled = True
    await plug.turn_off() if plug.is_on else await plug.turn_on()
    await device.update()
    button.disabled = False
    button.color = green if plug.is_on else red

# Toggle a plug
def toggle(device, button):
    asyncio.run_coroutine_threadsafe(toggle_async(device, button), loop)

# Toggle a plug's led
async def toggle_led_async(device, button):
    plug = led_button_plug[button]

    button.disabled = True
    await plug.set_led(False) if plug.led else await plug.set_led(True)
    await device.update()
    button.disabled = False
    button.color = green if plug.led else red


# Toggle a plug's led
def toggle_led(device, button):
    asyncio.run_coroutine_threadsafe(toggle_led_async(device, button), loop)


async def update_devices_async():
    tasks = [asyncio.create_task(device.update()) for device in devices]
    await asyncio.gather(*tasks)

    for button, plug in button_plug.items():
        button.color = green if plug.is_on else red
        button.disabled = False
    for led_button, plug in led_button_plug.items():
        led_button.color = green if plug.led else red
        led_button.disabled = False

def update_devices(delta_time):
    asyncio.run_coroutine_threadsafe(update_devices_async(), loop)
    pass


smart_plugs = []
smart_strips = []
async def init_devices():
    tasks = []
    for plug_ip in plug_ip_addresses:
        smart_plug = SmartPlug(plug_ip)
        devices.append(smart_plug)
        smart_plugs.append(smart_plug)
        tasks.append(asyncio.create_task(smart_plug.update()))
    for strip_ip in strip_ip_addresses:
        smart_strip = SmartStrip(strip_ip)
        devices.append(smart_strip)
        smart_strips.append(smart_strip)
        tasks.append(asyncio.create_task(smart_strip.update()))
    await asyncio.gather(*tasks)


class RootGrid(GridLayout):
    def __init__(self, **kwargs):
        super(RootGrid, self).__init__(**kwargs)
        self.cols = 2

        asyncio.run(init_devices())

        # Create buttons for plugs and their LEDs
        for smart_plug in smart_plugs:
            toggle_button = Button(
                text=smart_plug.alias,
                color = green if smart_plug.is_on else red,
            )
            toggle_button.bind(on_release=partial(toggle, smart_plug))
            button_plug[toggle_button] = smart_plug
            self.add_widget(toggle_button)

            toggle_led_button = Button(
                text='LED',
                color = green if smart_plug.led else red,
            )
            toggle_led_button.bind(on_release=partial(toggle_led, smart_plug))
            led_button_plug[toggle_led_button] = smart_plug
            self.add_widget(toggle_led_button)

        # Create buttons for strips
        for smart_strip in smart_strips:
            for plug in smart_strip.children:
                toggle_button = Button(
                    text=plug.alias,
                    color = green if plug.is_on else red,
                )
                toggle_button.bind(on_release=partial(toggle, smart_strip))
                button_plug[toggle_button] = plug
                self.add_widget(toggle_button)

        # Start the refresh clock
        Clock.schedule_interval(update_devices, 2)
                

class XHomeApp(App):
    def build(self):
        return RootGrid()

if __name__ == "__main__":
    XHomeApp().run()

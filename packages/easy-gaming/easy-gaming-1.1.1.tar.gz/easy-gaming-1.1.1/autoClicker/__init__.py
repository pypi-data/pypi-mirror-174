import mouse
import time
from pynput.keyboard import Key, Controller

keyboard = Controller()

def click(button, speed: float, duration: float, delay: float):
    time.sleep(delay)
    clicks = int(duration/speed)
    if button == 'left' or button == 'right' or button == 'middle':
        for i in range(0, clicks):
            mouse.click(button)
            time.sleep(speed)
    else:
        for i in range(0, clicks):
            keyboard.press(button)
            keyboard.release(button)
            time.sleep(speed)
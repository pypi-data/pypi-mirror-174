import mouse
import time
from screeninfo import get_monitors
import winsound

monitor = get_monitors()[0]

ver = []
hor = []

def record(delay: float, amount: float):
    if amount < 1:
        raise autoPosError("one or more action required")
    for i in range(0, amount):
        time.sleep(delay)
        pos = mouse.get_position()
        ver.append(round((pos[0]/monitor.width)*100, 2))
        hor.append(round((pos[1]/monitor.height)*100, 2))
        winsound.PlaySound("beep.wav", winsound.SND_FILENAME)
    with open('pos.txt','w') as sf:
        ver_2 = [str(x) for x in ver]
        ver_2 = " ".join(ver_2)
        hor_2 = [str(x) for x in hor]
        hor_2 = " ".join(hor_2)
        store = [ver_2, hor_2]
        sf.write(",".join(store))
    
def play(speed: float, delay: float, movespeed: float = 0.5, button = 'none'):
    ac = 0
    with open('pos.txt','r') as sf:
        time.sleep(delay)
        output = sf.read().split(',')
        ver = output[0].split(' ')
        hor = output[1].split(' ')
        ver_2 = [float(x) for x in ver]
        hor_2 = [float(x) for x in hor]
        for x in ver:
            time.sleep(movespeed)
            mouse.move((ver_2[ac] / 100) * monitor.width, (hor_2[ac] / 100) * monitor.height, duration = speed)
            if not button == "none":
                mouse.click(button)
            ac = ac + 1
    
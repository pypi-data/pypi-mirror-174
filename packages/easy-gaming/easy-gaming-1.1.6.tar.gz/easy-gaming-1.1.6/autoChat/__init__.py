import os
from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

if not os.path.isfile('saved-chats.txt'):
    with open('saved-chats.txt', 'w') as sv:
     sv.close()

def chat(delay: float, speed: float):
    data = []
    while True:
        autochat = input("What do you want to do? edit/play/view/exit ")
        if autochat == "edit" or autochat == "e":
            slot = int(input("What slot do you want to change? ")) - 1
            with open('saved-chats.txt', 'r') as sf:
                con = sf.read()
                if "," in con:
                    data = con.split(',')
            invar = input("What do you want to change it to? ")
            if slot > len(data):
                print("Please fill in the slot before first")
            else: 
                with open('saved-chats.txt', 'w') as sf:
                    if slot == len(data):
                        data.append(invar)
                    else:
                        data[slot] = invar
                    strdata = ",".join(data)
                    sf.write(strdata)
                    print("")
        if autochat == "play" or autochat == "p":
            with open('saved-chats.txt', 'r') as sf:
                con = sf.read()
                data = con.split(',')
            while True:
                slot = input("What slot do you want to play? save num/exit ")
                if not (slot == "exit" or slot == "e"):
                    slot = int(slot) - 1
                    a = data[slot]
                    b = [*a]
                    time.sleep(delay)
                    for x in range(len(b)):
                        keyboard.press(b[x])
                        keyboard.release(b[x])
                        time.sleep(speed)
                else:
                    print("")
                    time.sleep(0.1)
                    break
        if autochat == "view" or autochat == "v":
            with open('saved-chats.txt', 'r') as sf:
                con = sf.read()
                data = con.split(',')
            for x in data:
                print(x)
        if autochat == 'exit':
            print("")
            break

def spam(num: float, speed: float, delay: float):
    if input("Use at your own risk. proceed? y/n ") == "yes" or "y":
        time.sleep(delay)
        for i in range(0,num):
            keyboard.press(Key.ctrl)
            keyboard.press('v')
            keyboard.release(Key.ctrl)
            keyboard.release('v')
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            time.sleep(speed)

def reset():
    with open('saved-chats.txt', 'w') as sf:
        sf.write("")
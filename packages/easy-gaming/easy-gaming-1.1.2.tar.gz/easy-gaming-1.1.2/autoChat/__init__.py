import os
from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

if os.path.isfile('saved-chats.txt') == True:
    with open('saved-chats.txt', 'r') as sv:
        data = sv.read()
        con = data.split(',')
        if not len(con) == 5:
            sv.close()
            with open('saved-chats.txt', 'w') as sv:
                sv.write(',,,,')
else:
    with open('saved-chats.txt', 'w') as sv:
     sv.write(',,,,')

def chat(delay: float, speed: float):
    slot_1 = ""
    slot_2 = ""
    slot_3 = ""
    slot_4 = ""
    slot_5 = ""
    while True:
        autochat = input("What do you wan't to do? edit/play/view/exit ")
        if autochat == "edit" or "e":
            while True:
                slot = input("What slot do you wan't to change? 1..5/exit ")
                if slot == '1':
                    slot_1 = input("What message do you wan't to put in slot one? ")
                if slot == '2':
                    slot_2 = input("What message do you wan't to put in slot two? ")
                if slot == '3':
                    slot_3 = input("What message do you wan't to put in slot three? ")
                if slot == '4':
                    slot_4 = input("What message do you wan't to put in slot four? ")
                if slot == '5':
                    slot_5 = input("What message do you wan't to put in slot five? ")
                if slot == 'exit' or "e":
                    with open('saved-chats.txt', 'r') as sf:
                        data = sf.read()
                        con = data.split(',')
                        if slot_1 == "":
                            slot_1 = con[0]
                        if slot_2 == "":
                            slot_2 = con[1]
                        if slot_3 == "":
                            slot_3 = con[2]
                        if slot_4 == "":
                            slot_4 = con[3]
                        if slot_5 == "":
                            slot_5 = con[4]
                    with open('saved-chats.txt', 'w') as sf:
                        output = "{},{},{},{},{}".format(slot_1, slot_2, slot_3, slot_4, slot_5)
                        sf.write(output)
                    print("")
                    break
        if autochat == "play" or "p":
            with open('saved-chats.txt', 'r') as sf:
                data = sf.read()
                con = data.split(',')
                slot_1 = con[0]
                slot_2 = con[1]
                slot_3 = con[2]
                slot_4 = con[3]
                slot_5 = con[4]
            while True:
                slot = input("What slot do you wan't to play? 1..5/exit ")
                if slot == "1":
                    a = [*slot_1]
                    time.sleep(delay)
                    for x in range(len(a)):
                        keyboard.press(a[x])
                        keyboard.release(a[x])
                        time.sleep(speed)
                if slot == "2":
                    a = [*slot_2]
                    time.sleep(delay)
                    for x in range(len(a)):
                        keyboard.press(a[x])
                        keyboard.release(a[x])
                        time.sleep(speed)
                if slot == "3":
                    a = [*slot_3]
                    time.sleep(delay)
                    for x in range(len(a)):
                        keyboard.press(a[x])
                        keyboard.release(a[x])
                        time.sleep(speed)
                if slot == "4":
                    a = [*slot_4]
                    time.sleep(delay)
                    for x in range(len(a)):
                        keyboard.press(a[x])
                        keyboard.release(a[x])
                        time.sleep(speed)
                if slot == "5":
                    a = [*slot_5]
                    time.sleep(delay)
                    for x in range(len(a)):
                        keyboard.press(a[x])
                        keyboard.release(a[x])
                        time.sleep(speed)
                if slot == "exit" or "e":
                    print("")
                    break
        if autochat == "view" or "v":
            with open('saved-chats.txt', 'r') as sf:
                data = sf.read()
                con = data.split(',')
                slot_1 = con[0]
                slot_2 = con[1]
                slot_3 = con[2]
                slot_4 = con[3]
                slot_5 = con[4]
            if slot_1 == "":
                print("There is nothing in slot one")
            else:
                print("in slot one is: ", slot_1)
            if slot_2 == "":
                print("There is nothing in slot two")
            else:
                print("in slot two is: ", slot_2)
            if slot_3 == "":
                print("There is nothing in slot three")
            else:
                print("in slot three is: ", slot_3)
            if slot_4 == "":
                print("There is nothing in slot four")
            else:
                print("in slot four is: ", slot_4)
            if slot_5 == "":
                print("There is nothing in slot five")
            else:
                print("in slot five is: ", slot_5)
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
        sf.write(",,,,")
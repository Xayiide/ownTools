"""
pyxhook is the module that will give us access to the controler of the
key pressing
Credit to: https://github.com/JeffHoogland/pyxhook7

"""


import pyxhook
import time

log_file = '/home/xam/Documents/log_file'

def pressEvent(event):
    global running
    global log_file

    with open(log_file, 'a') as log:
        log.write(event.Key)
        log.write('\n')

    # If we press space, stop
    if event.Ascii == 32:
        running = False

# Create hook object
hook = pyxhook.HookManager()

# Listen to every key press and tell the object to use the function
# pressEvent() to handle what to do everytime a keystroke is detected
hook.KeyDown=pressEvent

# Hook the keyboard
hook.HookKeyboard()

# Start the hook
hook.start()

running = True
while running:
    time.sleep(0.1)

hook.cancel()

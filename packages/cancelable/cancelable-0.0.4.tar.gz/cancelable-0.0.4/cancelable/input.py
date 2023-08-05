import sys
import os

if os.name == 'nt':
    import msvcrt
else:
    import tty
    import termios
    import select

def InputHandler(prompt):
    if os.name == "nt":
        return InputHandlerWindows(prompt)
    else:
        return InputHandlerLinux(prompt)

_shouldCancel = False
canceled = False
def cancel():
    global _shouldCancel
    _shouldCancel = True
    while True:
        global canceled
        if canceled:
            break
    canceled = False
    return True

def shouldCancel():
    global _shouldCancel
    return _shouldCancel

def InputHandlerLinux(prompt):
    string = ""

    enabledSettings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno()) # Disable echo

    print(prompt, end='', flush=True)
    while True:
        if shouldCancel():
            break
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            char = sys.stdin.read(1)
            if char == "\n":
                break
            elif char == "\x7f":
                if len(string) > 0:
                    print("\b \b", end='', flush=True)
                string = string[:-1]
            else:
                string += char
                print(char, end='', flush=True)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, enabledSettings) # Enable echo
    print()

    global canceled
    canceled = True
    return string

def InputHandlerWindows(prompt):
    string = ""

    print(prompt, end='', flush=True)
    while True:
        if shouldCancel():
            break
        if msvcrt.kbhit():
            char = msvcrt.getwch()
            if char == "\r":
                break
            elif char == "\x08":
                if len(string) > 0:
                    print("\b \b", end='', flush=True)
                string = string[:-1]
            else:
                string += char
                print(char, end='', flush=True)

    print()

    global canceled
    canceled = True
    return string
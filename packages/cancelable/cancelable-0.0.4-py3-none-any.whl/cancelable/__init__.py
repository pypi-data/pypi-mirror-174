from cancelable import time, input
from cancelable import input as _input

time = time.TimeHandler
input = _input.InputHandler
cancelInput = _input.cancel
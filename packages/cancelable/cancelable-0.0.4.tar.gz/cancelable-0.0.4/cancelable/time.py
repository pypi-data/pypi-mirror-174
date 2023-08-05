import time as TIME

class TimeHandler:
    def sleep(seconds):
        global shouldCancelSleep
        shouldCancelSleep = False

        endSleep = TIME.time() + seconds
        while True:
            if shouldCancelSleep:
                break
            if TIME.time() >= endSleep:
                break

    def cancel():
        global shouldCancelSleep
        shouldCancelSleep = True
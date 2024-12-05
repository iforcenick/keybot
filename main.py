import pyautogui
import time
import threading
import random

# Interval in seconds to check for inactivity
CHECK_INTERVAL = .1
# Inactivity timeout in seconds before moving the mouse
INACTIVITY_TIMEOUT = 2 * 3600
# Minimum time in seconds between jiggles (3 hours)
JIGGLE_INTERVAL = 3 * 3600

# Track the last time the mouse was moved by the user and by the script
last_mouse_position = pyautogui.position()
last_active_time = time.time()
last_jiggle_time = 0

def check_inactivity():
    global last_mouse_position, last_active_time, last_jiggle_time

    while True:
        current_mouse_position = pyautogui.position()
        if current_mouse_position != last_mouse_position:
            last_mouse_position = current_mouse_position
            last_active_time = time.time()

        if (time.time() - last_active_time > INACTIVITY_TIMEOUT and
            time.time() - last_jiggle_time > JIGGLE_INTERVAL):

            jiggle_mouse()
            last_jiggle_time = time.time()

        time.sleep(CHECK_INTERVAL)

def jiggle_mouse():
    # Perform a "jiggle" by moving the mouse to a random nearby position
    x, y = pyautogui.position()

    # Random offsets to jiggle the mouse
    dx = random.randint(-1, 1)
    dy = random.randint(-1, 1)

    # Move the mouse to the new position and back
    pyautogui.moveTo(x + dx, y + dy, duration=0.1)

if __name__ == "__main__":
    # Start monitoring mouse activity in a separate thread
    activity_thread = threading.Thread(target=check_inactivity)
    activity_thread.daemon = True
    activity_thread.start()

    # Keep the main program running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
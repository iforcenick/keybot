import pyautogui
import time
import threading
import random
from datetime import datetime

# Interval in seconds to check for inactivity
CHECK_INTERVAL = 0.1
# Inactivity timeout in seconds before moving the mouse (2 hours)
# INACTIVITY_TIMEOUT = 2 * 60
INACTIVITY_TIMEOUT = 10

# Track the last time the mouse was moved by the user and by the script
last_mouse_position = pyautogui.position()
last_active_time = time.time()

WORK_START_HOUR = 9
WORK_END_HOUR = 23  # 5:00 PM in 24-hour format

def within_working_hours():
    now = datetime.now()
    return WORK_START_HOUR <= now.hour < WORK_END_HOUR

def check_inactivity():
    global last_mouse_position, last_active_time

    while True:
        if not within_working_hours():
            time.sleep(CHECK_INTERVAL)
            continue

        current_mouse_position = pyautogui.position()
        if current_mouse_position != last_mouse_position:
            last_mouse_position = current_mouse_position
            last_active_time = time.time()

        if (time.time() - last_active_time > INACTIVITY_TIMEOUT):
            jiggle_mouse()
            time.sleep(2)

        time.sleep(CHECK_INTERVAL)

def jiggle_mouse():
    x, y = pyautogui.position()
    print("[INFO] starting ...")

    for _ in range(5):  # Do 5 to 10 jiggles
        tx = x + random.randint(-100, 100)
        ty = y + random.randint(-100, 100)
        pyautogui.moveTo(tx, ty, duration=0.2)
        time.sleep(random.uniform(0.1, 0.3))
        current_mouse_position = pyautogui.position()
        if current_mouse_position.x != tx or current_mouse_position.y != ty:
            print("[INFO] stopping.")
            return

    pyautogui.moveTo(x, y, duration=0.2)
    print("[INFO] completed.")

if __name__ == "__main__":
    activity_thread = threading.Thread(target=check_inactivity)
    activity_thread.daemon = True
    activity_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
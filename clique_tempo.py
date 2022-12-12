import threading
from time import sleep
import pyautogui
import math

running = False

saved_x, saved_y = pyautogui.position()
count = 0

time_to_wait = 2 # in seconds
epsilon = 15
sleep_time = 0.05


def get_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


class CliqueTempo(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def mouse_not_moved(self, count):
        return count * sleep_time >= time_to_wait

    def run(self, root=None):
        global saved_x, saved_y, count, time_to_wait, epsilon, sleep_time
        print('bbb')
        current_x, current_y = pyautogui.position()
        print('current_x, current_y:', current_x, current_y)
        distance = get_distance(saved_x, saved_y, current_x, current_y)
        saved_x, saved_y = (current_x, current_y)
        print('distance', distance)
        if distance < epsilon:
            count = count + 1
            print(count)
            print(saved_x, saved_y)
            print("Mouse Movement # ", count)
        else:
            count = 0

        if self.mouse_not_moved(count):
            print('clicou')
            pyautogui.click()  
            count = 0
        sleep(sleep_time)
        print('aaa')
        if root:
            root.after(0, self.run(root))

    def activate(self):
        global running
        while running:
            self.run()

if __name__ == "__main__":
    running = True
    cliquetempo = CliqueTempo()
    cliquetempo.activate()
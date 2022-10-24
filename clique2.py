from time import sleep
import pyautogui
import math

saved_x, saved_y = pyautogui.position()
count = 0

time_to_wait = 5 # in seconds
epsilon = 5
sleep_time = 0.05


def get_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def mouse_not_moved(count):
    return count * sleep_time >= time_to_wait

def main():
    global saved_x, saved_y, count, time_to_wait, epsilon, sleep_time
    while True:
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

        if mouse_not_moved(count):
            print('clicou')
            pyautogui.click()  
            count = 0
        sleep(sleep_time)
        print('aaa')

if __name__ == "__main__":
    main()
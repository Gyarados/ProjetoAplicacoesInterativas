from dataclasses import dataclass
from multiprocessing.resource_sharer import stop
from screeninfo import get_monitors
import websocket
import _thread
import time
import rel
import json
import pyautogui
import math

pyautogui.FAILSAFE = False


@dataclass(frozen=True)
class MarkerInfo:
    timestamp: float
    success: bool
    translation_x: float = 0
    translation_y: float = 0
    translation_z: float = 0
    rotation_right_x: float = 0
    rotation_right_y: float = 0
    rotation_right_z: float = 0
    rotation_up_x: float = 0
    rotation_up_y: float = 0
    rotation_up_z: float = 0
    rotation_forward_x: float = 0
    rotation_forward_y: float = 0
    rotation_forward_z: float = 0


markers = [None, None]

h_size_pixels, v_size_pixels = pyautogui.size()
    
monitors = get_monitors()

h_size_cm, v_size_cm = (monitors[0].width_mm/10, monitors[0].height_mm/10)
print(h_size_cm, v_size_cm)

v_density = v_size_pixels / v_size_cm
h_density = h_size_pixels / h_size_cm
print(f"v_density: {v_density}, h_density: {h_density}")

message_counter = 0


def main():

    # Move mouse para o centro da tela:
    if len(monitors) != 1:
        return

    pyautogui.moveTo(h_size_pixels/2, v_size_pixels/2)

    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:5678",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()

def update_markers(marker_info: MarkerInfo):
    markers[0] = markers[1]
    markers[1] = marker_info

def get_coords():
    current_x, current_y = pyautogui.position()

    previous: MarkerInfo = markers[0]
    current: MarkerInfo = markers[1]

    delta_right = current.rotation_right_z - previous.rotation_right_z
    delta_up = current.rotation_up_z - previous.rotation_up_z

    z = (current.translation_z + previous.translation_z)/2
    
    delta_x = math.tan(delta_right*math.pi) * z
    delta_y = math.tan(delta_up*math.pi) * z
    
    # print(f"delta_x: {delta_x}, delta_y: {delta_y}")

    new_x = current_x - delta_x*h_density/10
    new_y = current_y - delta_y*v_density/10

    return new_x, new_y

def on_message(ws, message_json):

    start_time = time.perf_counter_ns()

    global message_counter

    if message_counter < 10:
        message_counter += 1
        return
    else:
        message_counter = 0

    message_dict = json.loads(message_json)
    marker_info = MarkerInfo(**message_dict)
    
    if not marker_info.success: 
        return
    
    update_markers(marker_info)

    x, y = get_coords()

    pyautogui.moveTo(x, y)

    stop_time = time.perf_counter_ns()

    print(f"Elapsed time: {(stop_time - start_time)/1e6} ms")
    # print(f"coords: {x}, {y}")
    
    # print(marker_info)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    main()

from dataclasses import dataclass
from screeninfo import get_monitors
import websocket
import rel
import json
import pyautogui
import math
import numpy as np

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


h_size_pixels, v_size_pixels = pyautogui.size()
    
monitors = get_monitors()

h_size_cm, v_size_cm = (monitors[0].width_mm/10, monitors[0].height_mm/10)
print(h_size_cm, v_size_cm)

v_density = v_size_pixels / v_size_cm
h_density = h_size_pixels / h_size_cm
print(f"v_density: {v_density}, h_density: {h_density}")

message_counter = 0

h_ref = h_size_pixels / 2
v_ref = v_size_pixels / 2

pi = math.pi


def main():

    # if len(monitors) != 1:
    #     return

    # Move mouse para o centro da tela:
    pyautogui.moveTo(h_ref, v_ref)

    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:5678",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()

def get_coords(current):

    delta_x = np.tan([current.rotation_right_z * pi])[0] * current.translation_z
    delta_y = np.tan([current.rotation_up_z * pi])[0] * current.translation_z
    
    new_x = h_ref - (current.translation_x + 0.1 * delta_x) * h_density
    new_y = v_ref + (current.translation_y - 0.1 * delta_y) * v_density

    return new_x, new_y

def on_message(ws, message_json):

    message_dict = json.loads(message_json)

    if not message_dict.get('success'):
        return

    global message_counter

    if message_counter < 5:
        message_counter += 1
        return
    else:
        message_counter = 0

        marker_info = MarkerInfo(**message_dict)

        x, y = get_coords(marker_info)

        pyautogui.moveTo(x, y)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    main()

from dataclasses import dataclass
import websocket
import _thread
import time
import rel
import json
import pyautogui
import math


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


markers = []


def main():

    # Move mouse para o centro da tela:
    h_size, v_size = pyautogui.size()
    pyautogui.moveTo(h_size/2, v_size/2)


    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:5678",
                              on_open=on_open,
                              on_message=on_message,
                            #   on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()

def update_markers(marker_info: MarkerInfo):
    markers[0] = markers[1]
    markers[1] = marker_info

def convert_coords():
    current_x, current_y = pyautogui.position()

    previous: MarkerInfo = markers[0]
    current: MarkerInfo = markers[1]

    delta_right = current.rotation_right_z - previous.rotation_right_z
    delta_up = current.rotation_up_z - previous.rotation_up_z
    delta_forward = current.rotation_forward_z - previous.rotation_forward_z

    hipotenuse = (current.translation_z + previous.translation_z)/2
    
    

    new_x = current_x + delta_x
    new_y = current_y + delta_y

    return new_x, new_y

def on_message(ws, message_json):
    message_dict = json.loads(message_json)
    marker_info = MarkerInfo(**message_dict)
    
    # if not marker_info.success: return
    
    update_markers(marker_info)

    x, y = convert_coords()

    # pyautogui.moveTo(x, y)
    print(f"coords: {x}, {y}")
    
    # print(marker_info)s

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    main()

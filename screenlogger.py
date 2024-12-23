from flask import Flask, Response
import cv2
import numpy as np
import mss
import pyautogui
import requests

# Define a server link to send the video stream
SERVER_URL = ""
# Function to capture the screen with mouse cursor and yield frames
def stream_to_server():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor
        while True:
            # Capture the screen
            screenshot = np.array(sct.grab(monitor))

            # Convert BGRA to BGR (OpenCV uses BGR)
            frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

            # Get the current mouse position
            mouse_x, mouse_y = pyautogui.position()

            # Draw the cursor (white circle)
            cursor_color = (255, 255, 255)  # White color
            cursor_radius = 5  # Circle radius
            cursor_thickness = -1  # Filled circle
            cv2.circle(frame, (mouse_x, mouse_y), cursor_radius, cursor_color, cursor_thickness)

            # Encode the frame in JPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes

            try:
                requests.post(SERVER_URL, data=buffer.tobytes(), headers={"Content-Type": "image/jpeg"})
            except requests.exceptions.RequestException as e:
                print(f"Failed to send frame: {e}")

if __name__ == '__main__':
    stream_to_server()

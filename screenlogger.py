import cv2
import mss
import numpy as np
import pyautogui
from flask import Flask, Response

# Flask application
app = Flask(__name__)


# Function to capture the screen with mouse cursor and yield frames
def generate_frames():
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
            frame_bytes = buffer.tobytes()

            # Yield as an MJPEG stream
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


# Route to serve the live stream

# TODO: Make this route private
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)

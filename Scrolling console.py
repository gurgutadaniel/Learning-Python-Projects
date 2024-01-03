import threading
import keyboard
import time
import ctypes
import tkinter as tk

scrolling_enabled = False
scroll_speed = 500
last_ctrl_press_time = 0
double_press_threshold = 0.5  # Adjust as needed (in seconds)

def toggle_scrolling():
    global scrolling_enabled
    scrolling_enabled = not scrolling_enabled
    update_status_label()

def update_status_label():
    if scrolling_enabled:
        status_label.config(text="Automatic scrolling: Enabled", font=("Helvetica", 12, "bold"), fg="red")
    else:
        status_label.config(text="Automatic scrolling: Disabled", font=("Helvetica", 12), fg="black")

def on_ctrl_press(e):
    global last_ctrl_press_time

    if e.event_type == keyboard.KEY_DOWN and e.name == 'ctrl':
        current_time = time.time()
        if current_time - last_ctrl_press_time < double_press_threshold:
            toggle_scrolling()

        last_ctrl_press_time = current_time

def on_right_click(e):
    global scrolling_enabled
    if e.event_type == keyboard.KEY_DOWN and e.name == 'right ctrl':
        toggle_scrolling()

def on_speed_change(value):
    global scroll_speed
    scroll_speed = int(value)

# Function to update scrolling speed in the scrolling thread
def update_scroll_speed():
    while True:
        if scrolling_enabled:
            # Use ctypes to send scroll input directly
            ctypes.windll.user32.mouse_event(0x800, 0, 0, -scroll_speed, 0)
        time.sleep(0.1)

# Tkinter GUI setup
root = tk.Tk()
root.title("Scrolling Controller")

status_label = tk.Label(root, text="Automatic scrolling: Disabled", font=("Helvetica", 12), fg="black")
status_label.pack(pady=10)

toggle_button = tk.Button(root, text="Toggle Scrolling", command=toggle_scrolling)
toggle_button.pack()

# Scale widget to adjust scrolling speed
speed_scale = tk.Scale(root, from_=1, to=1000, orient=tk.HORIZONTAL, label="Scroll Speed",
                       command=on_speed_change)
speed_scale.set(scroll_speed)  # Set the initial value
speed_scale.pack(pady=10)

# Register the Ctrl key press event
keyboard.hook_key('ctrl', on_ctrl_press)

# Register the right-click event
keyboard.hook_key('right ctrl', on_right_click)

# Start the scrolling thread
scrolling_thread = threading.Thread(target=update_scroll_speed)
scrolling_thread.daemon = True  # Set the thread as a daemon, so it will exit when the main program exits
scrolling_thread.start()

# Schedule status label updates
root.after(100, update_status_label)

# Run the Tkinter event loop
root.mainloop()

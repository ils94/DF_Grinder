import pyautogui
import keyboard
import tkinter as tk


def hold_button():
    button_to_hold = button_to_hold_entry.get()
    start_stop_key = start_stop_key_entry.get()

    def hold_action():
        if button_to_hold.lower() == 'left' or button_to_hold.lower() == 'right':
            pyautogui.mouseDown(button=button_to_hold.lower())
        else:
            pyautogui.keyDown(button_to_hold)

    def release_action():
        if button_to_hold.lower() == 'left' or button_to_hold.lower() == 'right':
            pyautogui.mouseUp(button=button_to_hold.lower())
        else:
            pyautogui.keyUp(button_to_hold)

    def on_key_event(event):
        if event.name == start_stop_key:
            if not hold_button.is_holding:
                hold_button.is_holding = True
                hold_action()
            else:
                hold_button.is_holding = False
                release_action()

    if not hasattr(hold_button, 'is_holding'):
        hold_button.is_holding = False

    # Unbind previous key events
    keyboard.unhook_all()

    # Bind new key events
    keyboard.on_press(on_key_event)
    keyboard.on_release(on_key_event)


def validate_entries(event=None):
    button_to_hold = button_to_hold_entry.get()
    start_stop_key = start_stop_key_entry.get()

    if button_to_hold and start_stop_key:
        hold_button.config(state=tk.NORMAL)
    else:
        hold_button.config(state=tk.DISABLED)


# Create the main window
window = tk.Tk()
window.title("DF Grinder")

# Calculate the screen dimensions
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the window position
window_width = 300
window_height = 150
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

window.geometry(f"{window_width}x{window_height}+{x}+{y}")
window.resizable(False, False)

# Find the icon file
icon_path = 'minigun.ico'
try:
    window.iconbitmap(icon_path)
except tk.TclError:
    pass  # Handle the missing icon file error gracefully

# Frame to hold widgets
frame = tk.Frame(window)
frame.pack(pady=20, anchor='w')

# Button/Key to Hold Label and Entry
button_to_hold_label = tk.Label(frame, text="Button/Key to Hold:")
button_to_hold_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
button_to_hold_entry = tk.Entry(frame)
button_to_hold_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')
button_to_hold_entry.bind('<KeyRelease>', validate_entries)

# Start/Stop Key Label and Entry
start_stop_key_label = tk.Label(frame, text="Start/Stop Key:")
start_stop_key_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
start_stop_key_entry = tk.Entry(frame)
start_stop_key_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')
start_stop_key_entry.bind('<KeyRelease>', validate_entries)

# Hold Button
hold_button = tk.Button(window, text="Save", width=8, height=1, command=hold_button, state=tk.DISABLED)
hold_button.pack(side='right', padx=10, pady=5)

# Start the main event loop
window.mainloop()

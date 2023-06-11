import pyautogui
import keyboard
import tkinter as tk


def hold_button():
    fire_key = fire_button_entry.get()
    trigger_key = trigger_key_entry.get()

    window.focus()

    # Save the values of the entries to a file
    with open('settings.txt', 'w') as file:
        file.write(f"FireKey:{fire_button_entry.get()}\n")
        file.write(f"TriggerKey:{trigger_key_entry.get()}")

    def hold_action():
        if fire_key.lower() == 'left' or fire_key.lower() == 'right':
            pyautogui.mouseDown(button=fire_key.lower())
        else:
            pyautogui.keyDown(fire_key)

    def release_action():
        if fire_key.lower() == 'left' or fire_key.lower() == 'right':
            pyautogui.mouseUp(button=fire_key.lower())
        else:
            pyautogui.keyUp(fire_key)

    def on_key_event(event):
        global script_enabled

        if script_enabled and event.name == trigger_key:
            if not save_button.is_holding:
                save_button.is_holding = True
                hold_action()
            else:
                save_button.is_holding = False
                release_action()

    if not hasattr(save_button, 'is_holding'):
        save_button.is_holding = False

    # Unbind previous key events
    keyboard.unhook_all()

    # Bind new key events
    keyboard.on_press(on_key_event)
    keyboard.on_release(on_key_event)


def toggle_script():
    global script_enabled

    if script_enabled:
        enable_button.config(text="Script: OFF", bg='red')
        script_enabled = False
    else:
        enable_button.config(text="Script: ON", bg='green')
        script_enabled = True


def validate_entries(event=None):
    button_to_hold = fire_button_entry.get()
    trigger_key = trigger_key_entry.get()

    if button_to_hold and trigger_key:
        save_button.config(state=tk.NORMAL)
        enable_button.config(state=tk.NORMAL)
    else:
        save_button.config(state=tk.DISABLED)
        enable_button.config(state=tk.DISABLED)


def load_settings():
    try:
        # Load the values from the file and set them in the entries
        with open('settings.txt', 'r') as file:
            for line in file:
                line = line.strip()
                key, value = line.split(':')
                if key == 'FireKey':
                    fire_button_entry.insert(0, value)
                elif key == 'TriggerKey':
                    trigger_key_entry.insert(0, value)
    except FileNotFoundError:
        pass


# Create the main window
window = tk.Tk()
window.title("DF Shooting Macro")

# Calculate the screen dimensions
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the window position
window_width = 270
window_height = 120
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

# LabelFrame to hold widgets
label_frame = tk.LabelFrame(window)
label_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Button/Key to Hold Label and Entry
fire_button_label = tk.Label(label_frame, text="Fire Button:")
fire_button_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
fire_button_entry = tk.Entry(label_frame)
fire_button_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')
fire_button_entry.bind('<KeyRelease>', validate_entries)

# Start/Stop Key Label and Entry
trigger_key_label = tk.Label(label_frame, text="Trigger Key:")
trigger_key_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
trigger_key_entry = tk.Entry(label_frame)
trigger_key_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')
trigger_key_entry.bind('<KeyRelease>', validate_entries)

# Hold Button
save_button = tk.Button(window, text="Save", width=8, height=1, command=hold_button, state=tk.DISABLED)
save_button.pack(side='right', padx=10, pady=5)

# Enable/Disable Script Button
script_enabled = False

enable_button = tk.Button(window, text="Script: OFF", width=12, height=1, command=toggle_script, state=tk.DISABLED,
                          bg='red')
enable_button.pack(side='left', padx=10, pady=5)

# Load settings from the file
load_settings()

# Start the main event loop
window.mainloop()

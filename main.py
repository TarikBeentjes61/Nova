import tkinter as tk
import threading
import time
import keyboard
from pynput import mouse
from PIL import Image, ImageDraw
import pystray

COMMANDS = [
    "help",
    "exit",
    "open",
    "close",
    "save",
    "delete",
    "copy",
    "paste",
    "undo",
    "redo",
    "search",
    "settings",
    "about",
]

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def fade_in(win, step=0.05):
    win.deiconify()
    win.lift()
    alpha = 0.0
    win.attributes("-alpha", alpha)
    while alpha < 1.0:
        alpha += step
        if alpha > 1: alpha = 1
        win.attributes("-alpha", alpha)
        time.sleep(0.02)
    win.focus_force()
    entry.focus_set()  # refocus entry after fade in

def fade_out(win, step=0.05):
    alpha = win.attributes("-alpha")
    while alpha > 0:
        alpha -= step
        if alpha < 0: alpha = 0
        win.attributes("-alpha", alpha)
        time.sleep(0.02)
    win.withdraw()

def show_window():
    if root.state() == "withdrawn":
        threading.Thread(target=fade_in, args=(root,), daemon=True).start()

def close_program(event=None):
    icon.stop()
    root.destroy()

def on_click(x, y, button, pressed):
    if pressed:
        x1 = root.winfo_rootx()
        y1 = root.winfo_rooty()
        x2 = x1 + root.winfo_width()
        y2 = y1 + root.winfo_height()

        if not (x1 <= x <= x2 and y1 <= y <= y2):
            if root.state() != 'withdrawn':
                threading.Thread(target=fade_out, args=(root,), daemon=True).start()

def start_mouse_listener():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

def update_list(*args):
    search_text = search_var.get().lower()
    filtered = [cmd for cmd in COMMANDS if search_text in cmd.lower()]

    listbox.delete(0, tk.END)

    if search_text == "" or not filtered:
        listbox.place_forget()
        root.geometry(f"{width}x{height}")
    else:
        for cmd in filtered:
            listbox.insert(tk.END, cmd)
        listbox.place(x=10, y=40, width=width - 20, height=100)
        root.geometry(f"{width}x{height + 110}")

def on_listbox_select(event):
    selection = event.widget.curselection()
    if selection:
        value = event.widget.get(selection[0])
        search_var.set(value)
        listbox.place_forget()
        root.geometry(f"{width}x{height}")
        print(f"Selected command: {value}")  # Real-time action: print selected command

def on_entry_key(event):
    if listbox.winfo_ismapped():
        if event.keysym == "Down":
            # Move selection down
            cur = listbox.curselection()
            if not cur:
                listbox.selection_set(0)
                listbox.activate(0)
            else:
                next_index = min(cur[0] + 1, listbox.size() - 1)
                listbox.selection_clear(0, tk.END)
                listbox.selection_set(next_index)
                listbox.activate(next_index)
            return "break"  # prevent cursor move in entry
        elif event.keysym == "Up":
            # Move selection up
            cur = listbox.curselection()
            if not cur:
                listbox.selection_set(0)
                listbox.activate(0)
            else:
                prev_index = max(cur[0] - 1, 0)
                listbox.selection_clear(0, tk.END)
                listbox.selection_set(prev_index)
                listbox.activate(prev_index)
            return "break"
        elif event.keysym == "Return":
            # Confirm selection
            cur = listbox.curselection()
            if cur:
                value = listbox.get(cur[0])
                search_var.set(value)
                listbox.place_forget()
                root.geometry(f"{width}x{height}")
                print(f"Confirmed command: {value}")  # Real-time action
            return "break"

# Start global mouse listener thread
threading.Thread(target=start_mouse_listener, daemon=True).start()

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-toolwindow", True)
root.configure(bg="white")

width, height = 300, 50
center_window(root, width, height)

search_var = tk.StringVar()
search_var.trace_add('write', update_list)

entry = tk.Entry(root, textvariable=search_var, font=("Arial", 14), bd=2, relief="solid")
entry.pack(fill="x", padx=10, pady=(10, 0))
entry.bind("<Down>", on_entry_key)
entry.bind("<Up>", on_entry_key)
entry.bind("<Return>", on_entry_key)
entry.focus()

listbox = tk.Listbox(root, font=("Arial", 12), bd=2, relief="solid",
                     selectbackground="#0078d7", selectforeground="white",
                     activestyle='none')
listbox.bind("<<ListboxSelect>>", on_listbox_select)

root.bind("<Escape>", close_program)

def hotkey_listener():
    keyboard.add_hotkey("ctrl+space", show_window)
    keyboard.wait()

threading.Thread(target=hotkey_listener, daemon=True).start()

root.withdraw()

def create_image():
    img = Image.new('RGB', (64, 64), "white")
    d = ImageDraw.Draw(img)
    d.ellipse((16, 16, 48, 48), fill="blue")
    return img

def on_quit(icon, item):
    close_program()

def on_show(icon, item):
    show_window()

icon = pystray.Icon("Spotlight", create_image(), "Quick Search", menu=pystray.Menu(
    pystray.MenuItem("Show", on_show),
    pystray.MenuItem("Exit", on_quit)
))
threading.Thread(target=icon.run, daemon=True).start()

root.mainloop()

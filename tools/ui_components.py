import tkinter as tk
from tkinter import ttk

def create_label_entry_frame(parent, label_text, default_value, on_change_callback=None):
    frame = tk.Frame(parent)
    frame.pack(anchor='w', fill='x', pady=(0, 10))

    label = tk.Label(frame, text=label_text, width=12, anchor='e')
    label.pack(side=tk.LEFT, padx=(0, 10))

    entry = tk.Entry(frame)
    entry.insert(tk.END, default_value)
    entry.pack(side=tk.LEFT, fill='x', expand=True)

    if on_change_callback:
        entry.bind("<FocusOut>", lambda event: on_change_callback())

    return entry

def create_button(parent, text, command):
    button = tk.Button(parent, text=text, command=command)
    button.pack(side=tk.RIGHT, padx=(10, 0))

def create_code_viewer(parent):
    code_viewer_frame = tk.Frame(parent)
    code_viewer_frame.pack(fill='both', expand=True)

    code_viewer = tk.Text(code_viewer_frame, wrap=tk.NONE)
    code_viewer.pack(side=tk.LEFT, fill='both', expand=True)

    scrollbar_y = ttk.Scrollbar(code_viewer_frame, orient=tk.VERTICAL, command=code_viewer.yview)
    scrollbar_y.pack(side=tk.RIGHT, fill='y')
    code_viewer.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=code_viewer.xview)
    scrollbar_x.pack(side=tk.BOTTOM, fill='x')
    code_viewer.configure(xscrollcommand=scrollbar_x.set)

    style = ttk.Style()
    style.configure("Custom.Vertical.TScrollbar", troughcolor="lightgray", background="lightgray")
    style.configure("Custom.Horizontal.TScrollbar", troughcolor="lightgray", background="lightgray")
    scrollbar_y.configure(style="Custom.Vertical.TScrollbar")
    scrollbar_x.configure(style="Custom.Horizontal.TScrollbar")

    return code_viewer
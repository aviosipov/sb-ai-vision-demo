import os
import tkinter as tk
from tkinter import filedialog, messagebox
from file_scanner import scan_and_generate
from config_handler import load_config, save_config
from ui_components import create_label_entry_frame, create_button, create_code_viewer

def browse_folder():
    current_folder = folder_entry.get()
    folder_path = filedialog.askdirectory(initialdir=current_folder)
    if folder_path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(tk.END, folder_path)
        save_config("folder_path", folder_path)

def start_scan():
    folder_path = folder_entry.get()
    file_extension = extension_entry.get()
    if folder_path and file_extension:
        scan_and_generate(folder_path, file_extension)
        save_config("file_extension", file_extension)
        display_file_content("scan_results.txt")
    else:
        messagebox.showwarning("Warning", "Please provide both folder path and file extension.")

def display_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            code_viewer.delete('1.0', tk.END)
            code_viewer.insert(tk.END, content)
    except IOError as e:
        messagebox.showerror("Error", f"Error reading file: {file_path}\nError details: {str(e)}")

# Create the main window
window = tk.Tk()
window.title("File Content Extractor")
window.geometry("600x600")
window.configure(padx=10, pady=10)
window.iconbitmap("icon.ico")

# Load configuration values
folder_path = load_config("folder_path", os.getcwd())
file_extension = load_config("file_extension", "py")

# Create and pack the widgets
folder_entry = create_label_entry_frame(window, "Folder Path:", folder_path, browse_folder)
create_button(folder_entry.master, "Browse", browse_folder)

extension_entry = create_label_entry_frame(window, "File Extension:", file_extension)

output_frame = tk.Frame(window)
output_frame.pack(anchor='w', fill='x', pady=(0, 10))

output_label = tk.Label(output_frame, text="Output File:")
output_label.pack(side=tk.LEFT, padx=(0, 10))

output_path = tk.Label(output_frame, text="scan_results.txt")
output_path.pack(side=tk.LEFT)

create_button(output_frame, "Start Scan", start_scan)

code_viewer = create_code_viewer(window)

# Start the Tkinter event loop
window.mainloop()
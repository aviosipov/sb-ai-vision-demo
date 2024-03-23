import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def scan_and_generate(folder_path, file_extension):
    output_file_name = "scan_results.txt"
    try:
        with open(output_file_name, 'w', encoding='utf-8') as output_file:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith(file_extension):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as input_file:
                                file_content = input_file.read()
                                output_file.write(f"{file_path}:\n")
                                output_file.write(file_content)
                                output_file.write("\n\n")
                        except (IOError, UnicodeDecodeError) as e:
                            print(f"Error reading file: {file_path}")
                            print(f"Error details: {str(e)}")
        messagebox.showinfo("Success", f"File '{output_file_name}' generated successfully.")
        display_file_content(output_file_name)
    except IOError as e:
        messagebox.showerror("Error", f"Error creating output file: {output_file_name}\nError details: {str(e)}")

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(tk.END, folder_path)

def start_scan():
    folder_path = folder_entry.get()
    file_extension = extension_entry.get()
    if folder_path and file_extension:
        scan_and_generate(folder_path, file_extension)
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
window.geometry("600x600")  # Set the window size (wider and taller)
window.configure(padx=10, pady=10)  # Add padding to the window

# Create and pack the widgets
input_frame = tk.Frame(window)
input_frame.pack(anchor='w', fill='x')

folder_label = tk.Label(input_frame, text="Folder Path:", width=12, anchor='e')
folder_label.pack(side=tk.LEFT, padx=(0, 10))

folder_entry = tk.Entry(input_frame)
folder_entry.insert(tk.END, os.getcwd())  # Set the default value to the current folder
folder_entry.pack(side=tk.LEFT, fill='x', expand=True)

browse_button = tk.Button(input_frame, text="Browse", width=10, command=browse_folder)
browse_button.pack(side=tk.RIGHT, padx=(10, 0))

input_frame.pack(pady=(0, 10))  # Add bottom margin to the input block

extension_frame = tk.Frame(window)
extension_frame.pack(anchor='w', fill='x')

extension_label = tk.Label(extension_frame, text="File Extension:", width=12, anchor='e')
extension_label.pack(side=tk.LEFT, padx=(0, 10))

extension_entry = tk.Entry(extension_frame)
extension_entry.insert(tk.END, "py")  # Set the default file extension to "py"
extension_entry.pack(side=tk.LEFT, fill='x', expand=True)

extension_frame.pack(pady=(0, 10))  # Add bottom margin to the input block

output_frame = tk.Frame(window)
output_frame.pack(anchor='w', fill='x')

output_label = tk.Label(output_frame, text="Output File:")
output_label.pack(side=tk.LEFT, padx=(0, 10))

output_path = tk.Label(output_frame, text="scan_results.txt")
output_path.pack(side=tk.LEFT)

scan_button = tk.Button(output_frame, text="Start Scan", command=start_scan)
scan_button.pack(side=tk.RIGHT, pady=(0, 10))

code_viewer_frame = tk.Frame(window)
code_viewer_frame.pack(fill='both', expand=True)

code_viewer = tk.Text(code_viewer_frame, wrap=tk.NONE)
code_viewer.pack(side=tk.LEFT, fill='both', expand=True)

scrollbar_y = ttk.Scrollbar(code_viewer_frame, orient=tk.VERTICAL, command=code_viewer.yview)
scrollbar_y.pack(side=tk.RIGHT, fill='y')
code_viewer.configure(yscrollcommand=scrollbar_y.set)

scrollbar_x = ttk.Scrollbar(window, orient=tk.HORIZONTAL, command=code_viewer.xview)
scrollbar_x.pack(side=tk.BOTTOM, fill='x')
code_viewer.configure(xscrollcommand=scrollbar_x.set)

style = ttk.Style()
style.configure("Custom.Vertical.TScrollbar", troughcolor="lightgray", background="lightgray")
style.configure("Custom.Horizontal.TScrollbar", troughcolor="lightgray", background="lightgray")
scrollbar_y.configure(style="Custom.Vertical.TScrollbar")
scrollbar_x.configure(style="Custom.Horizontal.TScrollbar")

# Start the Tkinter event loop
window.mainloop()
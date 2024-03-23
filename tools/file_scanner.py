import os
from tkinter import messagebox

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
    except IOError as e:
        messagebox.showerror("Error", f"Error creating output file: {output_file_name}\nError details: {str(e)}")
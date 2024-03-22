import os
import inquirer

def scan_and_generate(folder_path, file_extension):
    output_file_name = "scan_results.txt"
    print(f"Generating {folder_path}/*.{file_extension}")
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
        print(f"File '{output_file_name}' generated successfully.")
    except IOError as e:
        print(f"Error creating output file: {output_file_name}")
        print(f"Error details: {str(e)}")

def get_folder_choices(current_dir):
    subdirs = [d for d in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, d))]
    subdirs.sort()
    choices = subdirs + ['<< Go Back', 'Select Folder', 'Quit']
    questions = [
        inquirer.List(
            'folder',
            message=f"Select a folder (Current: {current_dir})",
            choices=choices,
        ),
    ]
    return inquirer.prompt(questions)['folder']

def get_file_extension():
    questions = [
        inquirer.Text(
            'extension',
            message="Enter the file extension (e.g., py):",
        ),
    ]
    return inquirer.prompt(questions)['extension']

def select_folder():
    folder = inquirer.text(message="Enter the folder path:")
    if os.path.isdir(folder):
        return folder
    else:
        print("Invalid folder path.")
        return None

def main():
    print("Welcome to the File Content Extractor!")
    print("This program scans a folder and generates a text file containing the contents of files with a specified extension.")
    print()

    current_dir = os.getcwd()

    while True:
        choices = ['<< Go Back', 'Select Folder', 'Quit']
        questions = [
            inquirer.List(
                'action',
                message=f"Select an action (Current: {current_dir})",
                choices=choices,
            ),
        ]
        selected_action = inquirer.prompt(questions)['action']

        if selected_action == '<< Go Back':
            parent_dir = os.path.dirname(current_dir)
            if parent_dir != current_dir:
                current_dir = parent_dir
            else:
                print("Already at the root directory.")
        elif selected_action == 'Select Folder':
            selected_folder = select_folder()
            if selected_folder:
                current_dir = selected_folder
            else:
                continue
        elif selected_action == 'Quit':
            break

        show_select_folder = True
        while True:
            subdirs = [d for d in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, d))]
            subdirs.sort()

            if subdirs:
                choices = subdirs + ['<< Go Back']
                if show_select_folder:
                    choices += ['Select Folder']

                questions = [
                    inquirer.List(
                        'folder',
                        message=f"Select a folder (Current: {current_dir})",
                        choices=choices,
                    ),
                ]
                selected_folder = inquirer.prompt(questions)['folder']

                if selected_folder == '<< Go Back':
                    show_select_folder = True
                    break
                elif selected_folder == 'Select Folder':
                    show_select_folder = False
                    file_extension = get_file_extension()
                    if not file_extension:
                        continue
                    scan_and_generate(current_dir, file_extension)
                    choice = inquirer.confirm("Do you want to scan another folder?")
                    if not choice:
                        return
                else:
                    current_dir = os.path.join(current_dir, selected_folder)
                    show_select_folder = True
                    continue
            else:
                break

        file_extension = get_file_extension()
        if not file_extension:
            continue

        scan_and_generate(current_dir, file_extension)

        choice = inquirer.confirm("Do you want to scan another folder?")
        if not choice:
            break

    print("Thank you for using the File Content Extractor!")







if __name__ == "__main__":
    main()
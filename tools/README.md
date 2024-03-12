# Folder Scanner

This repository contains a Python script for scanning a folder and generating a text file with the contents of files that have a specified extension.

## Features

- Interactive command-line interface for selecting folders and specifying file extensions
- Recursively scans subfolders within the selected folder
- Generates a text file (`scan_results.txt`) with the contents of files matching the specified extension
- Handles errors gracefully and provides informative error messages

## Requirements

- Python 3.x
- `inquirer` library (install using `pip install inquirer`)

## Usage

1. Clone the repository or download the `scan_folder.py` script.

2. Open a terminal or command prompt and navigate to the directory containing the script.

3. Run the script using the following command:
python scan_folder.py

4. The script will display a menu with options to select a folder, go back to the parent folder, or quit the program.

5. Navigate through the folders using the arrow keys and press Enter to select a folder.

6. If you choose "Select Folder," you will be prompted to enter the folder path manually.

7. After selecting a folder, enter the desired file extension (e.g., "py" for Python files) when prompted.

8. The script will scan the selected folder and its subfolders for files with the specified extension.

9. The contents of the matching files will be extracted and saved in a file named `scan_results.txt` in the same directory as the script.

10. After the scanning and file generation process is complete, you will be asked if you want to scan another folder. Enter "y" to scan again or "n" to exit the program.

## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).

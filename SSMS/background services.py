import os
import shutil

# Constants
MONITOR_FOLDER = r'C:\Users\Nikhil Sharma\Desktop\testing'
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")  # Default desktop path

def is_csv_or_excel(filename):
    _, ext = os.path.splitext(filename)
    return ext.lower() in ['.csv', '.xls', '.xlsx']

def prompt_user(filename):
    print(f"Non-CSV and Non-Excel file detected: {filename}")
    choice = input("Choose action - 'delete' or 'move' to desktop: ").lower()
    if choice == 'delete':
        os.remove(filename)
        print(f"File {filename} deleted.")
    elif choice == 'move':
        dest_file = os.path.join(DESKTOP_PATH, os.path.basename(filename))
        shutil.move(filename, dest_file)
        print(f"File {filename} moved to desktop.")
    else:
        print("Invalid choice. Skipping file.")

def monitor_folder():
    while True:
        for root, _, files in os.walk(MONITOR_FOLDER):
            for file in files:
                file_path = os.path.join(root, file)
                if not is_csv_or_excel(file_path):
                    prompt_user(file_path)

# Run the monitoring function
if __name__ == "__main__":
    monitor_folder()

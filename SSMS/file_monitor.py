import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCHED_FOLDER = r'C:\Users\Nikhil Sharma\Desktop\testing'
DESKTOP_FOLDER = os.path.join(os.path.expanduser("~"), 'Desktop')

def is_csv_or_excel(file):
    return file.endswith('.csv') or file.endswith('.xlsx') or file.endswith('.xls')

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.handle_file(event.src_path)
    
    def on_modified(self, event):
        if not event.is_directory:
            self.handle_file(event.src_path)
    
    def handle_file(self, file_path):
        if not is_csv_or_excel(file_path):
            if os.path.exists(os.path.join(DESKTOP_FOLDER, os.path.basename(file_path))):
                self.prompt_existing_file(file_path)
            else:
                self.prompt_action(file_path)
    
    def prompt_existing_file(self, file_path):
        print(f"File {os.path.basename(file_path)} already exists on Desktop.")
        action = input(f"Choose action for {file_path} - (D)elete or (M)ove to Desktop: ").strip().upper()
        if action == 'D':
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        elif action == 'M':
            new_path = os.path.join(DESKTOP_FOLDER, os.path.basename(file_path))
            os.rename(file_path, new_path)
            print(f"Moved to Desktop: {new_path}")
        else:
            print("Invalid action. Skipping file.")
    
    def prompt_action(self, file_path):
        print(f"File requires action: {file_path}")
        action = input(f"Choose action for {file_path} - (D)elete or (M)ove to Desktop: ").strip().upper()
        if action == 'D':
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        elif action == 'M':
            new_path = os.path.join(DESKTOP_FOLDER, os.path.basename(file_path))
            os.rename(file_path, new_path)
            print(f"Moved to Desktop: {new_path}")
        else:
            print("Invalid action. Skipping file.")

def monitor_folder():
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCHED_FOLDER, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    monitor_folder()

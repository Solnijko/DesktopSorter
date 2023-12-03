import os 
from re import findall
from pyuac import main_requires_admin
from time import sleep
from getpass import getuser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

desktop_path = os.path.dirname(f"C:\\Users\\{getuser()}\\Desktop\\")
desktop_path_scanned = os.scandir(desktop_path)
file_extension_pattern = r"\.([^.]+)$"
exec_count = 0

@main_requires_admin
def main():
    # Sort existing files

    event_handler = handleFiles()
    observer = Observer()
    observer.schedule(event_handler, path=desktop_path, recursive=False)

    observer.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

class handleFiles(FileSystemEventHandler):
    def on_created(self, event):
        print ("\n")
        sleep(5)
        file_path = event.src_path
        file_name = os.path.basename(file_path)
        file_extension = findall(file_extension_pattern, file_name)[0]

        if not event.is_directory:

            try:
                print(f"New file found: {file_name}")
                dest_path = desktop_path + "\\" + "." + file_extension + "\\"
                makeDir(dest_path)
                print(f"Moving a file {file_name} to {dest_path}" )
                os.replace(desktop_path + "\\" + file_name, (dest_path + file_name))

            except Exception as e:
                print(e)
                
def makeDir(path):
    os.makedirs(path, exist_ok=True)
    print("Made path: " + path)

if __name__ == "__main__":
    main() 
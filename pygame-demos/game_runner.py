import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class GameReloader(FileSystemEventHandler):
    def __init__(self):
        self.process = None

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f"Changes detected in {event.src_path}. Reloading the game...")
            self.reload_game()

    def reload_game(self):
        if self.process:
            self.process.terminate()
        self.process = subprocess.Popen(['python', 'falling_shapes.py'])

if __name__ == "__main__":
    path = '.'
    event_handler = GameReloader()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    # Run the game initially
    event_handler.reload_game()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
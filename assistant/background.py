import threading
import time
from queue import Queue

from assistant.voice import speak

class BackgroundTaskManager:
    def __init__(self):
        self.tasks = Queue()

        # Start the worker thread
        t = threading.Thread(target=self._worker, daemon=True)
        t.start()

    def add_task(self, name: str, func, *args, **kwargs):
        """Enqueue a new background task."""
        self.tasks.put((name, func, args, kwargs))
        speak(f"🔔 Started background task: {name}. I'll let you know when it's done.")

    def _worker(self):
        while True:
            name, func, args, kwargs = self.tasks.get()
            try:
                result = func(*args, **kwargs)
                speak(f"✅ Background task complete: {name}.")
            except Exception as e:
                speak(f"❌ Background task '{name}' failed: {e}")
            self.tasks.task_done()
            time.sleep(0.1)
import threading
import time
import uuid
import json
from queue import PriorityQueue
from assistant.voice import speak

class BackgroundTaskManager:
    def __init__(self, store_path="data/tasks.json"):
        self.store_path = store_path
        self.lock = threading.Lock()
        self.tasks = PriorityQueue()  # items: (priority, timestamp, task_id)
        self.metadata = {}            # task_id -> {name, status, ...}
        self._load_store()

        # Worker thread
        t = threading.Thread(target=self._worker, daemon=True)
        t.start()

    def _save_store(self):
        with self.lock, open(self.store_path, "w") as f:
            json.dump(self.metadata, f, default=str)

    def _load_store(self):
        try:
            with open(self.store_path) as f:
                self.metadata = json.load(f)
            # Re-enqueue any pending or running tasks for restart
            for tid, info in self.metadata.items():
                if info["status"] in ("pending", "running"):
                    self.tasks.put((info.get("priority", 5), info["timestamp"], tid))
        except FileNotFoundError:
            self.metadata = {}

    def add_task(self, name: str, func, *args, priority: int = 5, **kwargs) -> str:
        task_id = str(uuid.uuid4())[:8]
        timestamp = time.time()
        with self.lock:
            self.metadata[task_id] = {
                "name": name,
                "status": "pending",
                "priority": priority,
                "timestamp": timestamp,
                "result": None
            }
            self._save_store()
        self.tasks.put((priority, timestamp, task_id, func, args, kwargs))
        speak(f"🔔 Started background task #{task_id}: {name}")
        return task_id

    def cancel_task(self, task_id: str) -> bool:
        with self.lock:
            info = self.metadata.get(task_id)
            if not info or info["status"] != "pending":
                return False
            info["status"] = "cancelled"
            self._save_store()
            return True

    def list_tasks(self) -> list[dict]:
        with self.lock:
            return list(self.metadata.values())

    def get_status(self, task_id: str) -> dict | None:
        return self.metadata.get(task_id)

    def _worker(self):
        while True:
            try:
                priority, ts, task_id, func, args, kwargs = self.tasks.get()
            except ValueError:
                time.sleep(0.1)
                continue

            with self.lock:
                info = self.metadata.get(task_id)
                if not info or info["status"] != "pending":
                    continue  # skip cancelled or missing
                info["status"] = "running"
                self._save_store()

            try:
                result = func(*args, **kwargs)
                status = "done"
            except Exception as e:
                result = str(e)
                status = "failed"

            with self.lock:
                info = self.metadata[task_id]
                info["status"] = status
                info["result"] = result
                info["finished_at"] = time.time()
                self._save_store()

            speak(f"✅ Background task #{task_id} '{info['name']}' {status}.")

            self.tasks.task_done()
            time.sleep(0.1)
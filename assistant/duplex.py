# assistant/duplex.py

import threading
import time
from queue import Queue

from assistant.voice import listen_to_voice, speak

class DuplexManager:
    def __init__(self, agent_run_callback):
        self.agent_run_callback = agent_run_callback
        self.input_queue = Queue()
        self.output_queue = Queue()
        self.listening = threading.Event()
        self.speaking = threading.Event()
        self.stop_event = threading.Event()

    def _listen_loop(self):
        while not self.stop_event.is_set():
            if self.listening.is_set() and not self.speaking.is_set():
                try:
                    text = listen_to_voice()
                    if text:
                        self.input_queue.put(text)
                        self.listening.clear()
                except Exception as e:
                    print(f"[Duplex] Listening error: {e}")
            time.sleep(0.1)

    def _speak_loop(self):
        while not self.stop_event.is_set():
            if not self.output_queue.empty():
                text = self.output_queue.get()
                self.speaking.set()
                speak(text)
                self.speaking.clear()
                self.listening.set()
            time.sleep(0.1)

    def _agent_processing_loop(self):
        while not self.stop_event.is_set():
            if not self.input_queue.empty():
                task = self.input_queue.get()
                if task.lower() == "exit":
                    self.stop_event.set()
                    self.output_queue.put("Goodbye!")
                    break

                print(f"[Duplex] Processing task: {task}")
                response = self.agent_run_callback(task)
                # If agent.run() prints but returns None, you may want to capture output
                if isinstance(response, str):
                    self.output_queue.put(response)
            time.sleep(0.1)

    def start_duplex(self):
        """Begin the listening–processing–speaking threads."""
        self.listening.set()
        threads = [
            threading.Thread(target=self._listen_loop, daemon=True),
            threading.Thread(target=self._speak_loop, daemon=True),
            threading.Thread(target=self._agent_processing_loop, daemon=True),
        ]
        for t in threads:
            t.start()
        try:
            # Keep alive until stop_event is set
            while not self.stop_event.is_set():
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass
        print("[Duplex] Shutting down...")
        self.stop_event.set()
        for t in threads:
            t.join()
        print("[Duplex] Duplex mode stopped.")

# —————— Public entry point ——————
def start_duplex_conversation(agent):
    """
    Launch full–duplex voice mode.
    Pass in your Agent instance; we will call its .run(task) for each utterance.
    """
    manager = DuplexManager(agent.run)
    manager.start_duplex()
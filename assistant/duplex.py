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
            # Only listen if not speaking and listening is enabled
            if self.listening.is_set() and not self.speaking.is_set():
                try:
                    text = listen_to_voice()
                    if text:
                        self.input_queue.put(text)
                        self.listening.clear() # Stop listening after a command is received
                except Exception as e:
                    print(f"[Duplex] Listening error: {e}")
            time.sleep(0.1) # Small delay to prevent busy-waiting

    def _speak_loop(self):
        while not self.stop_event.is_set():
            if not self.output_queue.empty():
                text = self.output_queue.get()
                self.speaking.set()
                speak(text)
                self.speaking.clear()
                self.listening.set() # Resume listening after speaking is done
            time.sleep(0.1) # Small delay

    def _agent_processing_loop(self):
        while not self.stop_event.is_set():
            if not self.input_queue.empty():
                task = self.input_queue.get()
                if task.lower() == "exit":
                    self.stop_event.set()
                    self.output_queue.put("Goodbye!")
                    break
                
                print(f"[Duplex] Processing task: {task}")
                # Call the agent's run method and get its response
                response = self.agent_run_callback(task)
                self.output_queue.put(response) # Put the agent's response into the output queue for speaking
            time.sleep(0.1)

    def start_duplex(self):
        self.listening.set() # Start listening initially

        listen_thread = threading.Thread(target=self._listen_loop)
        speak_thread = threading.Thread(target=self._speak_loop)
        agent_thread = threading.Thread(target=self._agent_processing_loop)

        listen_thread.start()
        speak_thread.start()
        agent_thread.start()

        # Keep main thread alive until stop event is set
        while not self.stop_event.is_set():
            time.sleep(1)

        listen_thread.join()
        speak_thread.join()
        agent_thread.join()
        print("[Duplex] Duplex mode stopped.")
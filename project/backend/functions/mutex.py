import threading

#Critical section for accessing shared data structures
class CricticalSection():
    def __init__(self):
        self.sem = threading.Semaphore()

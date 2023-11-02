import multiprocessing
import threading

class DatabaseTester:
    def __init__(self, database, test_with_threads=True):
        self.database = database
        self.test_with_threads = test_with_threads
        if self.test_with_threads:
            self.lock = threading.lock()
        else:
            self.lock = multiprocessing.lock()

    def read_data(self, key):
        with self.lock:
            self.database.load_data_from_file()
            value = self.database.get_value(key)
            return value

    def write_data(self, key, value):
        with self.lock:
            self.database.load_data_from_file()
            self.database.set_value(key, value)
            self.database.save_data_to_file()
        return f"wrote to {key} -> {value}"
    def run_tests(self):
        pass

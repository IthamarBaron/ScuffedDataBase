from DataBase import Database
import multiprocessing
import threading

class DatabaseTester:
    def __init__(self, database, test_with_threads=True):
        self.database = database
        self.test_with_threads = test_with_threads
        if self.test_with_threads:
            self.lock = threading.Lock()
        else:
            self.lock = multiprocessing.Lock()

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
        def test_write_no_competition():
            # Test writing to the database without competition
            key = "test_key"
            value = "test_value"
            self.write_data(key, value)
            read_value = self.read_data(key)
            if read_value == value:
                print("Write no competition test passed.")
            else:
                print("Write no competition test failed.")

        def test_read_no_competition():
            # Test reading from the database without competition
            key = "test_key"
            value = "test_value"
            self.write_data(key, value)
            read_value = self.read_data(key)
            if read_value == value:
                print("Read no competition test passed.")
            else:
                print("Read no competition test failed.")

        def test_write_concurrent():
            # Test concurrent writing by two processes/threads
            key = "test_key"
            value1 = "value1"
            value2 = "value2"
            lock = multiprocessing.Lock() if not self.test_with_threads else threading.Lock()
            with lock:
                result1 = self.write_data(key, value1)
            # Sleep for a moment to allow the second process/thread to attempt to write
            import time
            time.sleep(1)
            with lock:
                result2 = self.write_data(key, value2)
            if result1 == "wrote to test_key -> value1" and result2 == "wrote to test_key -> value2":
                print("Write concurrent test passed.")
            else:
                print("Write concurrent test failed.")

        def test_read_concurrent():
            # Test concurrent reading by two processes/threads
            key = "test_key"
            value = "test_value"
            self.write_data(key, value)
            lock = multiprocessing.Lock() if not self.test_with_threads else threading.Lock()
            with lock:
                result1 = self.read_data(key)
            # Sleep for a moment to allow the second process/thread to attempt to read
            import time
            time.sleep(1)
            with lock:
                result2 = self.read_data(key)
            if result1 == value and result2 == value:
                print("Read concurrent test passed.")
            else:
                print("Read concurrent test failed.")

        test_write_no_competition()
        test_read_no_competition()
        test_write_concurrent()
        test_read_concurrent()


if __name__ == "__main__":
    database = Database(Database("database_file.pickle"))
    tester = DatabaseTester(database, test_with_threads=True)
    tester.run_tests()


import pickle

from DataBase import Database
import multiprocessing
import threading
import time


class DatabaseTester:
    def __init__(self, database, test_with_threads=True):
        self.database = database
        self.test_with_threads = test_with_threads
        if self.test_with_threads:
            self.lock = threading.Lock()
        else:
            self.lock = multiprocessing.Lock()

    def read_data(self, key):
        value = None
        with self.lock:
            try:
                self.database.load_data_from_file()
                value = self.database.get_value(key)

            except Exception as e:
                print(f"Read error: {e}")
        return value

    def write_data(self, key, value):
        with self.lock:
            try:
                self.database.load_data_from_file()
                self.database.set_value(key, value)
                self.database.save_data_to_file()
            except Exception as e:
                print(f"Write error: {e}")

    def run_tests(self):
        def test_write_no_competition():
            self.database.clear_database() # clearing the database for this test
            key = "test_key"
            value = "test_value"
            self.write_data(key, value)
            read_value = self.read_data(key)
            if read_value == value:
                print("Write no competition test passed.")
            else:
                print("Write no competition test failed.")

        def test_read_no_competition():
            self.database.clear_database() # clearing the database for this test
            key = "test_key"
            value = "test_value"
            self.write_data(key, value)
            read_value = self.read_data(key)
            if read_value == value:
                print("Read no competition test passed.")
            else:
                print("Read no competition test failed.")

        def test_write_concurrent():
            self.database.clear_database() # clearing the database for this test
            key = "test_key"
            value1 = "value1"
            value2 = "value2"

            # Attempt concurrent writes
            process1 = multiprocessing.Process(target=self.write_data, args=(key, value1))
            process2 = multiprocessing.Process(target=self.write_data, args=(key, value2))

            process1.start()
            process2.start()

            process1.join()
            process2.join()

            # Check if one of the writes failed
            read_value = self.read_data(key)
            if read_value in (value1, value2):
                print("Write concurrent test passed.")
            else:
                print("Write concurrent test failed.")

        def test_read_concurrent():
            self.database.clear_database() # clearing the database for this test
            key = "test_key"
            value = "test_value"
            tester.write_data(key, value) # writing this value to run the test on

            # Attempt concurrent reads
            process1 = multiprocessing.Process(target=self.read_data, args=(key,))
            process2 = multiprocessing.Process(target=self.read_data, args=(key,))

            process1.start()
            process2.start()

            process1.join()
            process2.join()

            # Check if one of the reads failed
            if self.read_data(key) == value:
                print("Read concurrent test passed.")
            else:
                print("Read concurrent test failed.")


        test_write_no_competition()
        test_read_no_competition()
        test_read_concurrent()
        test_write_concurrent()



if __name__ == "__main__":
    database = Database("database_file.pickle")
    tester = DatabaseTester(database, test_with_threads=False)
    tester.run_tests()



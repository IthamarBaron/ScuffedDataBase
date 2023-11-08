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
            self.database.clear_database()
            key = "test_key"
            value = "test_value"
            if self.test_with_threads:
                # Thread path
                thread = threading.Thread(target=self.write_data,args=(key,value,))
                thread.start()
                thread.join()

                read_value = self.read_data(key)
                if read_value == value:
                    print("Write no competition test passed (1).")
                else:
                    print("Write no competition test failed (1).")
            else:
                # Process path
                self.write_data(key, value)
                read_value = self.read_data(key)
                if read_value == value:
                    print("Write no competition test passed (1).")
                else:
                    print("Write no competition test failed (1).")

        def test_read_no_competition():
            self.database.clear_database()
            key = "test_key"
            value = "test_value"
            self.write_data(key,value)
            if self.test_with_threads:
                # Thread path
                def thread_read_data():
                    read_value = self.read_data(key)
                    if read_value == value:
                        print("Read no competition test passed (2).")
                    else:
                        print("Read no competition test failed (2).")

                self.write_data(key, value)
                thread = threading.Thread(target=thread_read_data)
                thread.start()
                thread.join()
            else:
                # Process path
                self.write_data(key, value)
                read_value = self.read_data(key)
                if read_value == value:
                    print("Read no competition test passed (2).")
                else:
                    print("Read no competition test failed (2).")

        def test_write_concurrent():
            self.database.clear_database()
            key = "test_key"
            value1 = "value1"
            value2 = "value2"
            if self.test_with_threads:
                # Thread path
                def thread_write_data(value):
                    self.write_data(key, value)

                thread1 = threading.Thread(target=thread_write_data, args=(value1,))
                thread2 = threading.Thread(target=thread_write_data, args=(value2,))
                thread1.start()
                thread2.start()
                thread1.join()
                thread2.join()

                read_value = self.read_data(key)
                if read_value in (value1, value2):
                    print("Write concurrent test passed (3).")
                else:
                    print("Write concurrent test failed (3).")
            else:
                # Process path
                process1 = multiprocessing.Process(target=self.write_data, args=(key, value1))
                process2 = multiprocessing.Process(target=self.write_data, args=(key, value2))

                process1.start()
                process2.start()

                process1.join()
                process2.join()

                # Check if one of the writes failed
                read_value = self.read_data(key)
                if read_value in (value1, value2):
                    print("Write concurrent test passed (3).")
                else:
                    print("Write concurrent test failed (3).")

        def test_multiple_readers():
            self.database.clear_database()
            key = "test_key"
            value = "test_value"
            if self.test_with_threads:
                # Thread path
                num_readers = 3
                results = []

                def thread_read_data():
                    read_value = self.read_data(key)
                    results.append(read_value)

                self.write_data(key, value)

                threads = []
                for _ in range(num_readers):
                    thread = threading.Thread(target=thread_read_data)
                    threads.append(thread)
                    thread.start()

                for thread in threads:
                    thread.join()

                if all(result == value for result in results):
                    print("Multiple readers test passed (4).")
                else:
                    print("Multiple readers test failed (4).")
            else:
                # Process path
                num_readers = 3
                results = []

                def process_read_data():
                    read_value = self.read_data(key)
                    results.append(read_value)

                self.write_data(key, value)

                processes = []
                for _ in range(num_readers):
                    process = multiprocessing.Process(target=self.read_data, args=(key,))
                    processes.append(process)
                    process.start()

                for process in processes:
                    process.join()

                if all(result == value for result in results):
                    print("Multiple readers test passed (4).")
                else:
                    print("Multiple readers test failed (4).")

        test_write_no_competition()
        test_read_no_competition()
        test_write_concurrent()
        test_multiple_readers()



if __name__ == "__main__":
    database = Database("database_file.pickle")
    tester = DatabaseTester(database, test_with_threads=False)
    tester.run_tests()



import pickle
import threading

class Database:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data_dict = {}
        self.lock = threading.Lock()

    def save_data_to_file(self):
        with open(self.file_path, 'wb') as database_file:
            pickle.dump(self.data_dict, database_file)
        pass

    def load_data_from_file(self):
        with open(self.file_path, 'rb') as database_file:
            self.data_dict = pickle.load(database_file)
        pass

    def set_value(self, key, value):
        # Implement the logic for setting a value in the database
        try:
            self.load_data_from_file()
            if key in self.data_dict.keys():
                self.data_dict[key] = value
                return f"Changed value in {key} to {value}."
            else:
                self.data_dict.update({key: value})
                return f"Added new pair Key:{key} Value:{value}."
            self.save_data_to_file()
        except:
            return "Something went wrong..."

    def get_value(self, key):
        # Implement the logic for getting a value from the database
        try:
            self.load_data_from_file()
            if key in self.data_dict.keys():
                return self.data_dict[key]
            else:
                return None
        except:
            return f"Something went wrong getting a value"

    def delete_value(self, key):
        # Implement the logic for deleting a value from the database
        try:
            self.load_data_from_file()
            del self.data_dict[key]
            self.save_data_to_file()
        except:
            return f"Something went wrong deleting data"



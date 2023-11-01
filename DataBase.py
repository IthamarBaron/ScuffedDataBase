import pickle
import threading

class Database:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data_dict = {}
        self.lock = threading.Lock()

    def save_data_to_file(self):
        # saves the data_dict to the datbase
        try:
            with open(self.file_path, 'wb') as database_file:
                pickle.dump(self.data_dict, database_file)
        except:
            pass

    def load_data_from_file(self):
        # loads the data_dict to the database
        try:
            with open(self.file_path, 'rb') as database_file:
                self.data_dict = pickle.load(database_file)
        except:
            pass

    def set_value(self, key, value):
        # the logic for setting a value in the database
        try:
            self.load_data_from_file()
            self.data_dict[key] = value
            self.save_data_to_file()
            return f"Set value in {key} to {value}."
        except Exception as e:
            return f"Something went wrong setting a value... [{e}]"

    def get_value(self, key):
        # the logic for getting a value from the database
        try:
            self.load_data_from_file()
            if key in self.data_dict.keys():
                return self.data_dict[key]
            else:
                return None
        except Exception as e:
            return f"Something went wrong getting a value... [{e}]"

    def delete_value(self, key):
        # the logic for deleting a value from the database
        try:
            self.load_data_from_file()
            del self.data_dict[key]
            self.save_data_to_file()
        except:
            return f"Something went wrong deleting data"



from LocalDict import HandleDict
import pickle
class Database(HandleDict):
    def __init__(self, file_path):
        super().__init__()  # Call the constructor of the parent class
        self.file_path = file_path

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


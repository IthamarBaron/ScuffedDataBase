# this file is used as a testing area
from LocalDict import HandleDict
from DataBase import Database

# Instantiate a Database object with a file path
db = Database("database_file.pickle")

# Test the set_value method
db.set_value("key1", "value1")
print(db.get_value("key1"))  # Should print "value1"

# Test the save and load methods
db.save_data_to_file()
db.load_data_from_file()

# Test the get_value method again after loading from the file
print(db.get_value("key1"))  # Should still print "value1"

# Test the delete_value method
db.delete_value("key1")
print(db.get_value("key1"))  # Should print None (key1 is deleted)

# Test saving and loading after deleting
db.save_data_to_file()
db.load_data_from_file()
print(db.get_value("key1"))  # Should still print None

# Test a new key-value pair
db.set_value("key2", "value2")
db.save_data_to_file()
db.load_data_from_file()
print(db.get_value("key2"))  # Should print "value2"

# Additional tests can be added as needed



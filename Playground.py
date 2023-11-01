# this file is used as a testing area
from DataBase import Database

import pickle
with open("database.pkl",'rb') as f:
    print(pickle.load(f))


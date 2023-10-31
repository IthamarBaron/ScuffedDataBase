# this file is used as a testing area
import pickle

class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def print_person(self):
        print(f"Name:{self.name}\nAge:{self.age}")



request = int(input("age to find:"))
cond = True
people = []
file = open("test.txt", 'rb')
while cond:
    try:
        person = pickle.load(file)
        if person.age == request:
            people.append(person)
    except Exception:
        cond = False
file.close()

for person in people:
    person.print_person()

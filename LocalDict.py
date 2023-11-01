
class HandleDict:
    def __init__(self):
        self.data_dict = {}

    def set_value(self, key, value):
        # the logic for setting a value in the database
        try:
            self.data_dict[key] = value
            return f"Set value in {key} to {value}."
        except Exception as e:
            return f"Something went wrong setting a value... [{e}]"

    def get_value(self, key):
        # the logic for getting a value from the database
        try:
            if key in self.data_dict.keys():
                return self.data_dict[key]
            else:
                return None
        except Exception as e:
            return f"Something went wrong getting a value... [{e}]"

    def delete_value(self, key):
        # the logic for deleting a value from the database
        try:
            del self.data_dict[key]
        except Exception as e:
            return f"Something went wrong deleting data[{e}]"



class Amenities:
    def __init__(self, list, address):
      self.list = list
      self.address = address

    def add_to_list(new_list):
        for key, value in new_list.items():
            if key in list:
                list[key] += value
            else:
                list[key] = value

    def get_list(self):
        return list


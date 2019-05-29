class RecursiveDefaultDict:

    def __init__(self):
        self.dict = {}

    def __getitem__(self, keys):
        return self.recursive_get(self.dict, keys)

    def recursive_get(self, dict_, keys):
        if len(keys) == 1:
            return dict_[keys]
        else:
            return self.recursive_get(dict_[keys[0]], keys[1:])

    def __setitem__(self, keys, value):
        self.recursive_set(self.dict, keys, value)

    def recursive_set(self, dict_, keys, value):
        #         print(dict_, keys, value)
        if not keys and value not in dict_:
            dict_[value] = None
        else:
            if keys[0] not in dict_ or dict_[keys[0]] is None:
                dict_[keys[0]] = {}
            self.recursive_set(dict_[keys[0]], keys[1:], value)

    def __str__(self):
        return str(self.dict)

    def to_dict(self):
        return self.dict

class User(object):
    def __init__(self, gender, age):
        self.gender = gender
        self.age = age
        self.queries = []

    def add_query(self, query):
        self.queries.append(query)

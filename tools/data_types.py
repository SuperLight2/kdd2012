class Query(object):
    def __init__(self, query_id):
        self.query_id = query_id
        self.ads = []

class User(object):
    def __init__(self, gender, age):
        self.gender = gender
        self.age = age
        self.queries = []

    def add_query(self, query):
        self.queries.append(query)

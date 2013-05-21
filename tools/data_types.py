class Instance(object):
    def __init__(self, line):
        s = line.strip().split('\t')
        self.clicks = int(s[0])
        self.impressions = int(s[1])
        self.displayURL = s[2]
        self.adID = s[3]
        self.advertiserID = s[4]
        self.depth = int(s[5])
        self.position = int(s[6])
        self.queryID = s[7]
        self.query_tokens = s[8].strip().split('|')
        self.keywordID = s[9]
        self.keyword_tokens = s[10].strip().split('|')
        self.titleID = s[11]
        self.title_tokens = s[12].strip().split('|')
        self.descriptionID = s[13]
        self.description_tokens = s[14].strip().split('|')
        self.userID = s[15]
        self.user_gender = int(s[16])
        self.user_age = int(s[17])


class Advertisement(object):
    def __init__(self, adId, advertiserID, depth, position, keywordID, keyword_tokens,
                 titleID, title_tokens, descriptionID, description_tokens):
        self.adID = adId
        self.advertiserID = advertiserID
        self.depth = depth
        self.position = position
        self.keywordID = keywordID
        self.keyword_tokens = keyword_tokens
        self.titleID = titleID
        self.title_tokens = title_tokens
        self.descriptionID = descriptionID
        self.description_tokens = description_tokens


class Query(object):
    def __init__(self, queryID, query_tokens):
        self.queryID = queryID
        self.query_tokens = query_tokens
        self.ads = []

    def add_instance(self, instance):
        self.ads.append(Advertisement(instance.adID, instance.advertiserID, instance.depth, instance.position,
                                      instance.keywordID, instance.keyword_tokens, instance.titleID,
                                      instance.title_tokens, instance.descriptionID, instance.description_tokens))


class User(object):
    def __init__(self, userID, gender, age):
        self.userID = userID
        self.gender = gender
        self.age = age
        self.queries_positions = {}
        self.queries = []

    def add_instance(self, instance):
        if instance.queryID not in self.queries_positions:
            self.queries.append(Query(instance.queryID, instance.query_tokens))
            self.queries_positions[instance.queryID] = len(self.queries)
        self.queries[instance.queryID].add_instance(instance)


class Object:
    def __init__(self, line):
        s = line.strip().split('\t')
        self.ctr = s[0]
        self.clicks = s[1]
        self.impressions = s[2]
        self.features = map(float, s[3:])
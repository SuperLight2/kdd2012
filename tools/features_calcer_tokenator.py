from feature_calcer import FeatureCalcer
from readers import InstanceReader
import random
import math


class FeatureCalcerTokenator(FeatureCalcer):
    def add_to_count(self, count, tokens):
        for word in tokens:
            if word not in count:
                count[word] = 0
            count[word] += 1

    def calc_tf(self, word, tokens):
        count = 0
        for w in tokens:
            if word == w:
                count += 1
        return 1.0 * count / len(tokens)

    def calc_tfidf(self, word, tokens, hash2idf):
        if word not in hash2idf:
            return 0
        return self.calc_tf(word, tokens) * hash2idf[word]

    def norm(self, vector):
        result = 0
        for v in vector:
            result += v * v
        return math.sqrt(result)

    def cosine(self, vector1, vector2):
        result = 0
        for i in xrange(len(vector1)):
            result += vector1[i] * vector2[i]
        result /= self.norm(vector1)
        result /= self.norm(vector2)
        return result

    def get_tf_idf_vector(self, tokens, hash2idf):
        result = []
        for marker_word in self.markers:
            result.append(self.calc_tfidf(marker_word, tokens, hash2idf))
        return result

    def get_tf_idf_vectors(self, instance):
        query_vector = self.get_tf_idf_vector(instance.query_tokens, self.hash2query_idf)
        title_vector = self.get_tf_idf_vector(instance.query_tokens, self.hash2title_idf)
        keyword_vector = self.get_tf_idf_vector(instance.query_tokens, self.hash2keyword_idf)
        description_vector = self.get_tf_idf_vector(instance.query_tokens, self.hash2description_idf)
        return query_vector, title_vector, keyword_vector, description_vector

    def get_instaces_similarity(self, instance1, instance2):
        vectors1 = self.get_tf_idf_vectors(instance1)
        vectors2 = self.get_tf_idf_vectors(instance2)
        return [self.cosine(vectors1[i], vectors2[i]) for i in xrange(len(vectors1))]

    def calc_statistics(self):
        count = {}
        for filepath in [self.training_filepath, self.test_filepath]:
            for instance in InstanceReader().open(filepath):
                for tokens in [instance.description_tokens, instance.keyword_tokens,
                              instance.query_tokens, instance.title_tokens]:
                    self.add_to_count(count, tokens)
        total_words = 0
        for word_count in count.values():
            total_words += word_count
        count = [(word, 1.0 * word_count / total_words) for word, word_count in count.iteritems()].sort(key=lambda x: -x[1])
        start = 5 * len(count) / 100
        self.markers = random.choice(count[start:start + 500])

        self.hash2prob = {}
        for word, prob in self.markers:
            self.hash2prob[word] = prob

        self.hash2query_idf = {}
        self.hash2title_idf = {}
        self.hash2keyword_idf = {}
        self.hash2description_idf = {}
        for word, _ in self.markers:
            self.hash2query_idf[word] = 0
            self.hash2title_idf[word] = 0
            self.hash2keyword_idf[word] = 0
            self.hash2description_idf[word] = 0

        instancesCount = 0
        self.support_instances = []
        for filepath in [self.training_filepath, self.test_filepath]:
            for instance in InstanceReader().open(filepath):
                if instance.clicks > 100:
                    if len(self.support_instances) == 10:
                        self.support_instances[random.randint(0, 10)] = self.support_instances[-1]
                    self.support_instances.append(instance)
                instancesCount += 1
                for marker_word, _ in self.markers:
                    for tokens, hash2idf in [(instance.query_tokens, self.hash2query_idf),
                                             (instance.title_tokens, self.hash2title_idf),
                                             (instance.keyword_tokens, self.hash2keyword_idf),
                                             (instance.description_tokens, self.hash2description_idf)]:
                        if marker_word in tokens:
                            hash2idf[marker_word] += 1.0
        for word, _ in self.markers:
            self.hash2query_idf[word] /= instancesCount
            self.hash2title_idf[word] /= instancesCount
            self.hash2keyword_idf[word] /= instancesCount
            self.hash2description_idf[word] /= instancesCount

    def calc_features(self, instance):
        vectors = self.get_tf_idf_vectors(instance)
        result = []
        for i in xrange(len(vectors)):
            for j in xrange(len(vectors)):
                if i < j:
                    result.append(self.cosine(vectors[i], vectors[j]))
        for support_instance in self.support_instances:
            result += self.get_instaces_similarity(support_instance, instance)
        return result

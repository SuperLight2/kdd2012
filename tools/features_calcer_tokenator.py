from feature_calcer import FeatureCalcer
from readers import InstanceReader
import random
from tools import cosine
import math


class FeatureCalcerTokenator(FeatureCalcer):
    def calc_tf(self, word, tokens):
        count = 0
        for w in tokens:
            if word == w:
                count += 1
        return 1.0 * count / len(tokens)

    def calc_tf_idf(self, word, tokens, hash2idf):
        if word not in hash2idf:
            return 0
        return self.calc_tf(word, tokens) * hash2idf[word]

    def get_markers_tf_idf_vector(self, tokens, hash2idf):
        result = []
        for marker_word in self.markers:
            result.append(self.calc_tf_idf(marker_word, tokens, hash2idf))
        return result

    def get_instance_vectors(self, instance):
        query_vector = self.get_markers_tf_idf_vector(instance.query_tokens, self.hash2query_idf)
        title_vector = self.get_markers_tf_idf_vector(instance.query_tokens, self.hash2title_idf)
        keyword_vector = self.get_markers_tf_idf_vector(instance.query_tokens, self.hash2keyword_idf)
        description_vector = self.get_markers_tf_idf_vector(instance.query_tokens, self.hash2description_idf)
        return query_vector, title_vector, keyword_vector, description_vector

    def get_instaces_similarity(self, instance1, instance2):
        vectors1 = self.get_instance_vectors(instance1)
        vectors2 = self.get_instance_vectors(instance2)
        return [cosine(vectors1[i], vectors2[i]) for i in xrange(len(vectors1))]

    def calc_statistics(self):
        word2count = dict()
        total_words = 0
        for filepath in [self.training_filepath, self.test_filepath]:
            for instance in InstanceReader().open(filepath):
                for tokens in [instance.description_tokens, instance.keyword_tokens,
                               instance.query_tokens, instance.title_tokens]:
                    for word in tokens:
                        if word not in word2count:
                            word2count[word] = 0
                        word2count[word] += 1
                        total_words += 1
        start = 5 * len(word2count) / 100
        count = [(word, 1.0 * word_count / total_words) for word, word_count in word2count.iteritems()].sort(
            key=lambda x: -x[1])
        self.markers = random.sample(count[start:start + 500], 100)

        self.hash2prob = dict()
        for word, prob in self.markers:
            self.hash2prob[word] = prob

        self.hash2query_idf = dict()
        self.hash2title_idf = dict()
        self.hash2keyword_idf = dict()
        self.hash2description_idf = dict()
        for word, _ in self.markers:
            self.hash2query_idf[word] = 0
            self.hash2title_idf[word] = 0
            self.hash2keyword_idf[word] = 0
            self.hash2description_idf[word] = 0

        instances_count = 0
        self.support_instances = []
        for filepath in [self.training_filepath, self.test_filepath]:
            for instance in InstanceReader().open(filepath):
                if instance.clicks > 100:
                    if len(self.support_instances) == 10:
                        self.support_instances[random.randint(0, 10)] = self.support_instances.pop(-1)
                    self.support_instances.append(instance)
                instances_count += 1
                for marker_word, _ in self.markers:
                    for tokens, hash2idf in [(instance.query_tokens, self.hash2query_idf),
                                             (instance.title_tokens, self.hash2title_idf),
                                             (instance.keyword_tokens, self.hash2keyword_idf),
                                             (instance.description_tokens, self.hash2description_idf)]:
                        if marker_word in tokens:
                            hash2idf[marker_word] += 1.0
        for word, _ in self.markers:
            self.hash2query_idf[word] = math.log(instances_count / self.hash2query_idf[word])
            self.hash2title_idf[word] = math.log(instances_count / self.hash2title_idf[word])
            self.hash2keyword_idf[word] = math.log(instances_count / self.hash2keyword_idf[word])
            self.hash2description_idf[word] = math.log(instances_count / self.hash2description_idf[word])

    def calc_features(self, instance):
        vectors = self.get_instance_vectors(instance)
        result = []
        for i in xrange(len(vectors)):
            for j in xrange(len(vectors)):
                if i < j:
                    result.append(cosine(vectors[i], vectors[j]))
        for support_instance in self.support_instances:
            result += self.get_instaces_similarity(support_instance, instance)
        return result

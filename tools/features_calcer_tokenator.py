from feature_calcer import FeatureCalcer
from readers import InstanceReader
import random
from tools import cosine, calc_tf_idf
import math


class FeatureCalcerTokenator(FeatureCalcer):
    def get_markers_tf_idf_vector(self, tokens, hash2idf):
        result = []
        for marker_word in self.markers:
            result.append(calc_tf_idf(marker_word, tokens, hash2idf))
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
        count = sorted([(word, 1.0 * word_count / total_words) for word, word_count in word2count.iteritems()],
                       key=lambda x: (-x[1], x[0]))
        self.markers = random.sample(count[start:start + 500], 100)

        self.hash2prob = dict()
        for word, prob in self.markers:
            self.hash2prob[word] = prob

        self.hash2query_idf = dict()
        self.hash2title_idf = dict()
        self.hash2keyword_idf = dict()
        self.hash2description_idf = dict()

        instances_count = 0
        self.support_instances = []
        for filepath in [self.training_filepath, self.test_filepath]:
            for instance in InstanceReader().open(filepath):
                if instance.clicks > 100:
                    if len(self.support_instances) == 10:
                        self.support_instances[random.randint(0, 9)] = self.support_instances[9]
                        self.support_instances.pop(-1)
                    self.support_instances.append(instance)
                instances_count += 1
                for marker_word, _ in self.markers:
                    for tokens, hash2idf in [(instance.query_tokens, self.hash2query_idf),
                                             (instance.title_tokens, self.hash2title_idf),
                                             (instance.keyword_tokens, self.hash2keyword_idf),
                                             (instance.description_tokens, self.hash2description_idf)]:
                        if marker_word in tokens:
                            if marker_word not in hash2idf:
                                hash2idf[marker_word] = 0
                            hash2idf[marker_word] += 1.0
        for word, _ in self.markers:
            if word in self.hash2query_idf:
                self.hash2query_idf[word] = math.log(instances_count / self.hash2query_idf[word])
            if word in self.hash2title_idf:
                self.hash2title_idf[word] = math.log(instances_count / self.hash2title_idf[word])
            if word in self.hash2keyword_idf:
                self.hash2keyword_idf[word] = math.log(instances_count / self.hash2keyword_idf[word])
            if word in self.hash2description_idf:
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


class FeatureCalcerTokenatorLight(FeatureCalcer):
    def get_markers_tf_idf_vector(self, tokens, hash2idf):
        result = []
        for marker_word in self.markers:
            result.append(calc_tf_idf(marker_word, tokens, hash2idf))
        return result

    def get_instance_vectors(self, instance):
        return self.get_markers_tf_idf_vector(instance.query_tokens, self.hash2idf)

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
        start = 3 * len(word2count) / 100
        count = sorted([(word, 1.0 * word_count / total_words) for word, word_count in word2count.iteritems()],
                       key=lambda x: (-x[1], x[0]))
        self.markers = random.sample(count[start:start + 200], 100)

        self.hash2prob = dict()
        for word, prob in self.markers:
            self.hash2prob[word] = prob

        self.hash2idf = dict()
        instances_count = 0
        for filepath in [self.training_filepath, self.test_filepath]:
            for instance in InstanceReader().open(filepath):
                instances_count += 1
                for marker_word, _ in self.markers:
                    for tokens in [instance.query_tokens, instance.title_tokens, instance.keyword_tokens, instance.description_tokens]:
                        if marker_word in tokens:
                            if marker_word not in self.hash2idf:
                                self.hash2idf[marker_word] = 0
                            self.hash2idf[marker_word] += 1.0
        for word, _ in self.markers:
            if word in self.hash2idf:
                self.hash2idf[word] = math.log(instances_count / self.hash2idf[word])

    def calc_features(self, instance):
        vectors = self.get_instance_vectors(instance)
        result = []
        for i in xrange(len(vectors)):
            for j in xrange(len(vectors)):
                if i < j:
                    result.append(cosine(vectors[i], vectors[j]))
        return result

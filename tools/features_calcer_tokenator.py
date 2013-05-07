from feature_calcer import FeatureCalcer
from readers import InstanceReader
import random
from tools import cosine, calc_tf_idf
import math


class FeatureCalcerTokenator(FeatureCalcer):
    def get_markers_tf_idf_vector(self, tokens, hash2idf):
        result = []
        for marker_word, _ in self.markers:
            result.append(calc_tf_idf(marker_word, tokens, hash2idf))
        return result

    def get_instance_vectors(self, instance):
        query_vector = self.get_markers_tf_idf_vector(instance.query_tokens, self.hash2idf)
        title_vector = self.get_markers_tf_idf_vector(instance.title_tokens, self.hash2idf)
        keyword_vector = self.get_markers_tf_idf_vector(instance.keyword_tokens, self.hash2idf)
        description_vector = self.get_markers_tf_idf_vector(instance.description_tokens, self.hash2idf)
        return query_vector, title_vector, keyword_vector, description_vector

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
        """
        cosine between tf-idf token vectors: query, title
        cosine between tf-idf token vectors: query, keyword
        cosine between tf-idf token vectors: query, description
        cosine between tf-idf token vectors: title, keyword
        cosine between tf-idf token vectors: title, description
        cosine between tf-idf token vectors: keyword, description
        query tokens idf`s sum
        title tokens idf`s sum
        keyword tokens idf`s sum
        description tokens idf`s sum
        """
        vectors = self.get_instance_vectors(instance)
        result = []
        for i in xrange(len(vectors)):
            for j in xrange(len(vectors)):
                if i < j:
                    result.append(cosine(vectors[i], vectors[j]))
        for tokens in [instance.query_tokens, instance.title_tokens, instance.keyword_tokens, instance.description_tokens]:
            weight_sum = 0
            for word in tokens:
                weight = 0
                if word in self.hash2idf:
                    weight = self.hash2idf[word]
                weight_sum += weight
            result.append(weight_sum)
        return result

from decision_tree import DecisionTree
from collections import defaultdict
from histogram import Histogram
from impurity import GiniFunction, EntropyFunction
from regularization import zero, log_regularization
import random
from tools.readers import ObjectReader
from tools.data_types import Object

import logging
_logger = logging.getLogger(__name__)


def get_classes_count(data, indexes):
    result = defaultdict(int)
    for index in indexes:
        result[data[index][0]] += 1
    return result


def get_class_from_object(learning_object):
    try:
        if float(learning_object.clicks) > 0:
            return '1'
        return '0'
    except ValueError:
        return learning_object.ctr


class SimpleClassifier:
    def __init__(self, discretization=8, alpha=0.9, min_object_in_node=-1, impurity_function=EntropyFunction):
        self.discretization = discretization
        self.alpha = alpha
        self.min_object_in_node = min_object_in_node
        self.impurity_function = impurity_function

    def learn(self, features_filepath):
        decision_tree = DecisionTree()
        current_node_index = decision_tree.get_next_non_terminal_node()
        node2indexes = defaultdict(list)
        data = []
        original_G = None

        _logger.debug("Reading data")
        index = 0
        features_count = None
        for current_object in ObjectReader().open(features_filepath):
            original_class = get_class_from_object(current_object)
            features = current_object.features
            if features_count is None:
                features_count = len(features)
            data.append((original_class, features))
            node2indexes[current_node_index].append(index)
            index += 1
        _logger.debug("End reading data")

        while decision_tree.get_next_non_terminal_node() is not None:
            current_node_index = decision_tree.get_next_non_terminal_node()
            data_indexes = node2indexes[current_node_index]
            _logger.debug("Current node index: " + str(current_node_index))
            _logger.debug("Indexes count:" + str(len(data_indexes)))

            current_G = self.impurity_function.calc(get_classes_count(data, data_indexes))
            _logger.debug("Current G: " + str(current_G))
            if original_G is None:
                original_G = current_G
            if (current_G < self.alpha * original_G) or (len(data_indexes) < self.min_object_in_node):
                _logger.debug("Stop in node")
                class_probabilities = dict()
                for index in data_indexes:
                    cls = data[index][0]
                    if cls not in class_probabilities:
                        class_probabilities[cls] = 0
                    class_probabilities[cls] += 1
                decision_tree.set_node_classification(current_node_index, class_probabilities)
                continue

            splits = []
            for feature_index in xrange(features_count):
                values = sorted([data[index][1][feature_index] for index in data_indexes], key=lambda x: float(x))
                for j in xrange(self.discretization):
                    splits.append((feature_index, values[j * len(values) / self.discretization]))

            max_delta = None
            best_feature_index = None
            best_split_threshold = None
            for feature_index, split_threshold in splits:
                left_indexes = []
                right_indexes = []
                for index in data_indexes:
                    if data[index][1][feature_index] < split_threshold:
                        left_indexes.append(index)
                    else:
                        right_indexes.append(index)
                left_G = self.impurity_function.calc(get_classes_count(data, left_indexes))
                right_G = self.impurity_function.calc(get_classes_count(data, right_indexes))
                tau = 1.0 * len(left_indexes) / len(data_indexes)
                delta = current_G - tau * left_G - (1 - tau) * right_G
                if (max_delta is None) or (delta > max_delta):
                    max_delta = delta
                    best_feature_index = feature_index
                    best_split_threshold = split_threshold
            _logger.debug("Best feature index: " + str(best_feature_index))
            _logger.debug("Best split threshold: " + str(best_split_threshold))
            _logger.debug("Max delta: " + str(max_delta))

            left_child, right_child = decision_tree.split_node(current_node_index, best_feature_index,
                                                               best_split_threshold)
            left_indexes = []
            right_indexes = []
            for index in data_indexes:
                if data[index][1][best_feature_index] < best_split_threshold:
                    left_indexes.append(index)
                else:
                    right_indexes.append(index)
            node2indexes[left_child] = left_indexes
            node2indexes[right_child] = right_indexes
        return decision_tree


class SPDRWorker:
    def __init__(self, bins_count=30):
        self.data = list()
        self.node2indexes = defaultdict(list)
        self.decision_tree = DecisionTree()
        self.histograms = dict()
        self.bins_count = bins_count

    def add_object(self, original_class, features):
        index = len(self.data)
        self.data.append((original_class, features))
        node_index = self.decision_tree.navigate(features)
        self.node2indexes[node_index].append(index)
        self.update_histogram_in_tree(node_index, original_class, features)

    def get_histogram(self, node_index, feature_index, class_key):
        if node_index not in self.histograms:
            self.histograms[node_index] = dict()
        if feature_index not in self.histograms[node_index]:
            self.histograms[node_index][feature_index] = dict()
        if class_key not in self.histograms[node_index][feature_index]:
            self.histograms[node_index][feature_index][class_key] = Histogram(self.bins_count)
        return self.histograms[node_index][feature_index][class_key]

    def split_node(self, node_index, feature_index, split_threshold):
        self.clear_histograms(node_index)
        left_child, right_child = self.decision_tree.split_node(node_index, feature_index, split_threshold)
        for index in self.node2indexes[node_index]:
            class_key, features = self.data[index]
            if features[feature_index] < split_threshold:
                self.node2indexes[left_child].append(index)
                self.update_histogram_in_tree(left_child, class_key, features)
            else:
                self.node2indexes[right_child].append(index)
                self.update_histogram_in_tree(right_child, class_key, features)

    def update_histogram_in_tree(self, node_index, original_class, features):
        for feature_index in xrange(len(features)):
            self.get_histogram(node_index, feature_index, original_class).add(features[feature_index])

    def get_classes_from_node_index(self, node_index):
        result = defaultdict(int)
        for index in self.node2indexes[node_index]:
            result[self.data[index][0]] += 1
        return result

    def clear_histograms(self, node_index):
        if node_index in self.histograms:
            del(self.histograms[node_index])


class SPDTClassifier:
    def __init__(self, workers_count=30, discretization=8, alpha=0.8, min_object_in_node=400,
                 impurity_function=GiniFunction, worker_bins_count=30, regularization=log_regularization):
        self.discretization = discretization
        self.alpha = alpha
        self.min_object_in_node = min_object_in_node
        self.impurity_function = impurity_function
        self.workers_count = workers_count
        self.worker_bins_count = worker_bins_count
        self.regularization = regularization

    def learn(self, features_filepath):
        decision_tree = DecisionTree()
        workers = [SPDRWorker(self.worker_bins_count) for _ in xrange(self.workers_count)]
        original_G = None
        features_count = None
        classes = set()

        _logger.debug("Reading data")
        for current_object in ObjectReader().open(features_filepath):
            original_class = get_class_from_object(current_object)
            features = current_object.features
            if features_count is None:
                features_count = len(features)
            classes.add(original_class)
            workers[random.randint(0, self.workers_count - 1)].add_object(original_class, features)
        _logger.debug("End reading data")

        while decision_tree.get_next_non_terminal_node() is not None:
            current_node_index = decision_tree.get_next_non_terminal_node()
            _logger.debug("Current node: " + str(current_node_index))

            histograms = []
            feature_histogram = []
            for feature_index in xrange(features_count):
                histograms.append(dict())
                feature_histogram.append(Histogram(self.worker_bins_count))
                for class_key in classes:
                    if class_key not in histograms[feature_index]:
                        histograms[feature_index][class_key] = Histogram(self.worker_bins_count)
                    for worker in workers:
                        histograms[feature_index][class_key].merge(worker.get_histogram(current_node_index,
                                                                                        feature_index, class_key))
                    feature_histogram[feature_index].merge(histograms[feature_index][class_key])

            classes_in_node_index = defaultdict(int)
            total_elements = 0
            for class_key in classes:
                classes_in_node_index[class_key] = histograms[0][class_key].get_total_elements()
                total_elements += histograms[0][class_key].get_total_elements()
            _logger.debug("Total elements: " + str(total_elements))
            for worker in workers:
                worker.clear_histograms(current_node_index)
            decision_tree.set_node_classification(current_node_index, classes_in_node_index)
            if not total_elements:
                raise BaseException("Fuck!")

            current_G = self.impurity_function.calc(classes_in_node_index)
            current_R = self.regularization(classes_in_node_index)
            _logger.debug("Impurity: " + str(current_G))
            _logger.debug("Regularization: " + str(current_R))
            if original_G is None:
                original_G = current_G
            if (current_G < self.alpha * original_G) or (total_elements < self.min_object_in_node):
                _logger.debug("Stop in node, total elements: " + str(total_elements))
                continue

            splits = []
            for feature_index in xrange(features_count):
                min_value, max_value = feature_histogram[feature_index].get_min_max_elements()
                values = feature_histogram[feature_index].uniform(self.discretization + 1)
                for value in values:
                    if (min_value < value) and (value < max_value):
                        splits.append((feature_index, value))
            max_delta = None
            best_feature_index = None
            best_split_threshold = None
            for feature_index, split_threshold in splits:
                tau = feature_histogram[feature_index].sum(split_threshold) / feature_histogram[feature_index].get_total_elements()
                classes_in_left = dict()
                classes_in_right = dict()
                for class_key in histograms[feature_index]:
                    classes_in_left[class_key] = 0
                    classes_in_right[class_key] = histograms[feature_index][class_key].get_total_elements()
                    if histograms[feature_index][class_key].get_total_elements() > 0:
                        classes_in_left[class_key] = histograms[feature_index][class_key].sum(split_threshold)
                        classes_in_right[class_key] -= classes_in_left[class_key]
                left_R = self.regularization(classes_in_left)
                right_R = self.regularization(classes_in_right)
                delta = current_G - tau * (self.impurity_function.calc(classes_in_left) + left_R) - (1 - tau) * (self.impurity_function.calc(classes_in_right) + right_R)
                if (max_delta is None) or (max_delta < delta):
                    max_delta = delta
                    best_feature_index = feature_index
                    best_split_threshold = split_threshold
            _logger.debug("Best feature index: " + str(best_feature_index))
            _logger.debug("Best split threshold: " + str(best_split_threshold))
            _logger.debug("Max delta: " + str(max_delta))

            if (max_delta is not None) or (max_delta > 0):
                decision_tree.split_node(current_node_index, best_feature_index, best_split_threshold)
                for worker in workers:
                    worker.split_node(current_node_index, best_feature_index, best_split_threshold)
        return decision_tree
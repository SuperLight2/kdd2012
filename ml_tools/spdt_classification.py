from decision_tree import DecisionTree
from collections import defaultdict
import math

import logging
_logger = logging.getLogger(__name__)


def gini_index(data, indexes):
    q = dict()
    for index in indexes:
        cls = data[index][0]
        if cls not in q:
            q[cls] = 0
        q[cls] += 1
    result = 1
    for cls_elements in q.values():
        result -= (1.0 * cls_elements / len(indexes)) ** 2
    return result


def empirical_emtropy(data, indexes):
    q = dict()
    for index in indexes:
        cls = data[index][0]
        if cls not in q:
            q[cls] = 0
        q[cls] += 1
    result = 0
    for cls_elements in q.values():
        p = 1.0 * cls_elements / len(indexes)
        if abs(p) > 1e-15:
            result -= p * math.log(p)
    return result


def train_classifier_tree(features_filepath,
                          SPLIT_COUNT=8, ALPHA=0.7, MIN_OBJECTS_COUNT=30, IMPURITY_FUNCTION=empirical_emtropy):
    decision_tree = DecisionTree()
    current_node_index = decision_tree.get_next_non_terminal_node()
    node2indexes = defaultdict(list)
    data = []
    original_G = None

    _logger.debug("Reading data")
    index = 0
    features_count = None
    for line in open(features_filepath):
        s = line.strip().split('\t')
        object_class = s[0]
        features = map(float, s[1:])
        if features_count is None:
            features_count = len(features)
        data.append((object_class, features))
        node2indexes[current_node_index].append(index)
        index += 1
    _logger.debug("End reading data")

    while decision_tree.get_next_non_terminal_node() is not None:
        current_node_index = decision_tree.get_next_non_terminal_node()
        data_indexes = node2indexes[current_node_index]
        _logger.debug("Current node index: " + str(current_node_index))
        _logger.debug("Indexes count:" + str(len(data_indexes)))

        splits = []
        for feature_index in xrange(features_count):
            values = sorted([data[index][1][feature_index] for index in data_indexes], key=lambda x: float(x))
            for j in xrange(SPLIT_COUNT):
                splits.append((feature_index, values[j * len(values) / SPLIT_COUNT]))

        left_child, right_child = decision_tree.split_node(current_node_index, 0, 0)
        current_G = IMPURITY_FUNCTION(data, data_indexes)
        _logger.debug("Current G: " + str(current_G))
        if original_G is None:
            original_G = current_G
        if (current_G < ALPHA * original_G) or (len(data_indexes) < MIN_OBJECTS_COUNT):
            _logger.debug("Stop in node")
            class_probabilities = dict()
            for index in data_indexes:
                cls = data[index][0]
                if cls not in class_probabilities:
                    class_probabilities[cls] = 0
                class_probabilities[cls] += 1
            decision_tree.set_node_classification(current_node_index, class_probabilities)
            continue

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
            left_G = IMPURITY_FUNCTION(data, left_indexes)
            right_G = IMPURITY_FUNCTION(data, right_indexes)
            tau = 1.0 * len(left_indexes) / len(data_indexes)
            delta = current_G - tau * left_G - (1 - tau) * right_G
            if (max_delta is None) or (delta > max_delta):
                max_delta = delta
                best_feature_index = feature_index
                best_split_threshold = split_threshold
        _logger.debug("Best feature index: " + str(best_feature_index))
        _logger.debug("Best split threshold: " + str(best_split_threshold))
        _logger.debug("Max delta: " + str(max_delta))

        decision_tree.nodes[current_node_index].feature_index = best_feature_index
        decision_tree.nodes[current_node_index].split_threshold = best_split_threshold
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
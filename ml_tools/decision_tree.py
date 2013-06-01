import pickle
from node import Node


class DecisionTree(object):
    def __init__(self):
        self.nodes = [Node()]
        self.info = dict()

    def split_node(self, node_index, feature_index, split_threshold):
        self.nodes[node_index].feature_index = feature_index
        self.nodes[node_index].split_threshold = split_threshold
        self.nodes[node_index].node_type = Node.CONDITION_NODE
        self.nodes[node_index].left_child = len(self.nodes)
        self.nodes.append(Node())
        self.nodes[node_index].right_child = len(self.nodes)
        self.nodes.append(Node())
        return len(self.nodes) - 2, len(self.nodes) - 1

    def set_node_classification(self, node_index, class_probabilities=None):
        self.nodes[node_index].node_type = Node.CLASSIFICATION_NODE
        self.nodes[node_index].class_probabilities = class_probabilities.copy()
        total = 0.0
        for value in class_probabilities.values():
            total += value
        for key in self.nodes[node_index].class_probabilities.keys():
            self.nodes[node_index].class_probabilities[key] /= total
        if self.nodes[node_index].left_child is not None:
            self.nodes[self.nodes[node_index].left_child].node_type = Node.ZOMBIE_NODE
        if self.nodes[node_index].right_child is not None:
            self.nodes[self.nodes[node_index].right_child].node_type = Node.ZOMBIE_NODE

    def get_next_non_terminal_node(self):
        for node_index in xrange(len(self.nodes)):
            if self.nodes[node_index].node_type == Node.NON_TERMINAL_NODE:
                return node_index
        return None

    def navigate(self, features):
        current = 0
        while self.nodes[current].node_type == Node.CONDITION_NODE:
            if features[self.nodes[current].feature_index] < self.nodes[current].split_threshold:
                current = self.nodes[current].left_child
            else:
                current = self.nodes[current].right_child
        return current

    def navigate_to_node(self, features):
        return self.nodes[self.navigate(features)]

    def calc_mc(self, features):
        return self.navigate_to_node(features).class_probabilities


def save_to_file(decision_tree, filepath):
    pickle.dump(decision_tree, filepath)


def load_from_file(filepath):
    return pickle.load(filepath)
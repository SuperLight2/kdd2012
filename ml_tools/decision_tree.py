import pickle
from node import Node

class DecisionTree(object):
    def __init__(self):
        self.nodes = [Node()]
        self.info = dict()

    """
    END_INFO = "END_INFO"

    @classmethod
    def serilize_from_file(cls, opened_file):
        current_node = None
        for line in opened_file:
            line = line.strip()
            if not line:
                continue
            if line == DecisionTree.Node.BEGIN_NODE:
                current_node = DecisionTree.Node(0)
            elif line == DecisionTree.Node.END_NODE:
                return current_node
            elif line == "class_probabilities":
                _, dictionary = line.strip('\t')
                dictionary = dictionary.strip(',')
                for word in dictionary:
                    key, value = word.strip().split(':')
                    current_node.class_probabilities[int(key)] = float(value)
            else:
                key, value = line.split('\t')
                setattr(current_node, key, value)
                if key in ['left_child', 'right_child', 'feature_index']:
                    setattr(current_node, key, int(value))
                if key in ['split_threshold', 'value']:
                    setattr(current_node, key, float(value))

    def set_property(self, key, value):
        self.info[key] = value

    def save_to_file(self, filepath):
        f_out = open(filepath, 'w')
        for key, value in self.info.iteritems():
            print >> f_out, "%s\t%s" % (key, value)
        print >> f_out, DecisionTree.END_INFO
        for node in self.nodes:
            print >> f_out, node.serialize_to_string()

    def load_from_file(self, filepath):
        f_in = open(filepath)
        for line in f_in:
            if line == DecisionTree.END_INFO:
                break
        self.nodes = []
        while True:
            current_node = DecisionTree.Node.serilize_from_file(f_in)
            if current_node is None:
                break
            self.nodes.append(current_node)
        self.nodes.sort(key=lambda node: int(node.self_index))"""

    def split_node(self, node_index, feature_index, split_threshold):
        self.nodes[node_index].feature_index = feature_index
        self.nodes[node_index].split_threshold = split_threshold
        self.nodes[node_index].node_type = Node.CONDITION_NODE
        self.nodes[node_index].left_child = len(self.nodes)
        self.nodes.append(Node())
        self.nodes[node_index].right_child = len(self.nodes)
        self.nodes.append(Node())
        return len(self.nodes) - 2, len(self.nodes) - 1

    def set_node_classification(self, node_index, class_probabilities):
        self.nodes[node_index].node_type = Node.CLASSIFICATION_NODE
        self.nodes[node_index].class_probabilities = class_probabilities
        total = 0.0
        for value in class_probabilities.values():
            total += value
        for key in self.nodes[node_index].class_probabilities.keys():
            self.nodes[node_index].class_probabilities[key] /= total
        if self.nodes[node_index].left_child is not None:
            self.nodes[self.nodes[node_index].left_child].node_type = Node.ZOMBIE_NODE
        if self.nodes[node_index].right_child is not None:
            self.nodes[self.nodes[node_index].right_child].node_type = Node.ZOMBIE_NODE

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

    def get_next_non_terminal_node(self):
        for node_index in xrange(len(self.nodes)):
            if self.nodes[node_index].node_type == Node.NON_TERMINAL_NODE:
                return node_index
        return None

    def calc_mc(self, features):
        return self.navigate_to_node(features).class_probabilities


def save_to_file(decision_tree, filepath):
    pickle.dump(decision_tree, filepath)

def load_from_file(filepath):
    return pickle.load(filepath)
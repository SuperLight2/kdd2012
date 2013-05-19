class Node(object):
    NON_TERMINAL_NODE = '1'
    REGRESSION_NODE = '2'
    CLASSIFICATION_NODE = '3'
    ZOMBIE_NODE = '4'
    CONDITION_NODE = '5'

    def __init__(self, node_type=NON_TERMINAL_NODE, left_child=None, right_child=None, feature_index=None,
                 split_threshold=None):
        self.node_type = node_type
        self.left_child = left_child
        self.right_child = right_child
        self.feature_index = feature_index
        self.split_threshold = split_threshold
        self.class_probabilities = dict()

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

    """
        BEGIN_NODE = 'BEGIN_NODE'
        END_NODE = 'END_NODE'

        def serialize_to_string(self):
            result = DecisionTree.Node.BEGIN_NODE
            result += "\nnode_type\t%s" % str(self.node_type)
            result += "\nleft_child\t%s" % str(self.left_child)
            result += "\nright_child\t%s" % str(self.right_child)
            result += "\nfeature_index\t%s" % str(self.feature_index)
            result += "\nsplit_threshold\t%s" % str(self.split_threshold)
            result += "\nclass_probabilities\t%s" % str(",".join(map(str, ["%s:%s" % (key, str(value))
                                                                           for key, value in
                                                                           self.class_probabilities.iteritems()])))
            result += "\n" + DecisionTree.Node.END_NODE
            return result
    """

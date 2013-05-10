NON_TERMINAL_NODE = '1'
REGRESSION_NODE = '2'
CLASSIFICATION_NODE = '3'


class DesicionTree(object):
    END_INFO = "END_INFO"

    class Node(object):
        BEGIN_NODE = 'BEGIN_NODE'
        END_NODE = 'END_NODE'

        def __init__(self, index, node_type=NON_TERMINAL_NODE):
            self.self_index = index
            self.node_type = node_type
            self.left_child = None
            self.right_child = None
            self.feature_index = None
            self.split_threshold = None
            self.value = None
            self.class_probabilities = dict()

        def is_in_condition(self, features):
            return features[self.feature_index] < self.split_threshold

        def serialize_to_string(self):
            result = DesicionTree.Node.BEGIN_NODE
            result += "\nself_infex\t%s" % str(self.self_index)
            result += "\nnode_type\t%s" % str(self.node_type)
            result += "\nleft_child\t%s" % str(self.left_child)
            result += "\nright_child\t%s" % str(self.right_child)
            result += "\nfeature_index\t%s" % str(self.feature_index)
            result += "\nsplit_threshold\t%s" % str(self.split_threshold)
            result += "\nvalue\t%s" % str(self.value)
            result += "\nclass_probabilities\t%s" % str(",".join(map(str, ["%s:%s" % (str(key), str(value))
                                                                           for key, value in
                                                                           self.class_probabilities.iteritems()])))
            result += "\n" + DesicionTree.Node.END_NODE
            return result

        @classmethod
        def serilize_from_file(cls, opened_file):
            current_node = None
            for line in opened_file:
                line = line.strip()
                if not line:
                    continue
                if line == DesicionTree.Node.BEGIN_NODE:
                    current_node = DesicionTree.Node(0)
                elif line == DesicionTree.Node.END_NODE:
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
                    if key in ['self_index', 'left_child', 'right_child', 'feature_index']:
                        setattr(current_node, key, int(value))
                    if key in ['split_threshold', 'value']:
                        setattr(current_node, key, float(value))

    def __init__(self):
        self.nodes = [DesicionTree.Node(0)]
        self.info = dict()

    def set_property(self, key, value):
        self.info[key] = value

    def save_to_file(self, filepath):
        f_out = open(filepath, 'w')
        for key, value in self.info.iteritems():
            print >> f_out, "%s\t%s" % (key, value)
        print >> f_out, DesicionTree.END_INFO
        for node in self.nodes:
            print >> f_out, node.serialize_to_string()

    def load_from_file(self, filepath):
        f_in = open(filepath)
        for line in f_in:
            if line == DesicionTree.END_INFO:
                break
        self.nodes = []
        while True:
            current_node = DesicionTree.Node.serilize_from_file(f_in)
            if current_node is None:
                break
            self.nodes.append(current_node)
        self.nodes.sort(key=lambda node: int(node.self_index))

    def split_node(self, node_index, feature_index, split_threshold):
        self.nodes[node_index].feature_index = feature_index
        self.nodes[node_index].split_threshold = split_threshold
        self.nodes[node_index].left_child = len(self.nodes)
        self.nodes.append(self.Node(len(self.nodes)))
        self.nodes[node_index].right_child = len(self.nodes)
        self.nodes.append(self.Node(len(self.nodes)))

    def navigate(self, features):
        current = 0
        while self.nodes[current].node_type == NON_TERMINAL_NODE:
            if self.nodes[current].is_in_condition(features):
                current = self.nodes[current].left_child
            else:
                current = self.nodes[current].right_child
        return current

    def calc(self, features):
        return self.nodes[self.navigate(features)].value

    def calc_mc(self, features):
        return self.nodes[self.navigate(features)].class_probabilities
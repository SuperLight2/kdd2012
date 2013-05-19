from tools.tools import gcd

def GCD(A, B):
    while True:
        r = A.x % B.x
        if r == 0:
            return B.x
        A.x = B.x
        B.x = r


class C():
    X = list([1, 2, 3])
    X.append(4)



def main():
    C.X[2] = 11
    print C.X
    d = dict()
    d[(0, 1)] = 1
    d[(1, 1)] = 2
    d[(1, 1)] += 2
    print d


if __name__ == '__main__':
    main()

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


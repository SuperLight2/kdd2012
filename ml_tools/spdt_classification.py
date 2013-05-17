from decision_tree import DecisionTree

def train_decision_tree(features_filepath):
    decision_tree = DecisionTree()
    for line in open(features_filepath):
        s = line.strip().split('\t')
        ctr = float(s[0])
        features = map(float, s[1:])

    return decision_tree
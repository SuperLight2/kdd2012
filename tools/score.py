import math
from score_tools import *


class ScoreCalcer(object):
    def __init__(self, solution_file, submission_file, type_filter=None, delimiter=','):
        self.num_clicks, self.num_impressions, self.types = read_solution_file(solution_file, delimiter)
        self.predicted_ctr = read_submission_file(submission_file, delimiter)
        if type_filter is not None:
            self.num_clicks = [self.num_clicks[i] for i in xrange(len(self.num_clicks)) if self.types[i] == type_filter]
            self.num_impressions = [self.num_impressions[i] for i in xrange(len(self.num_impressions)) if self.types[i] == type_filter]
            self.predicted_ctr = [self.predicted_ctr[i] for i in xrange(len(self.predicted_ctr)) if self.types[i] == type_filter]

    def score_AUC(self):
        return scoreClickAUC(self.num_clicks, self.num_impressions, self.predicted_ctr)

    def score_NWMAE(self):
        return scoreNWMAE(self.num_clicks, self.num_impressions, self.predicted_ctr)

    def score_WRMSE(self):
        return scoreWRMSE(self.num_clicks, self.num_impressions, self.predicted_ctr)


class WilcoxonTest(object):
    def __init__(self, X1, X2, eps=1e-7):
        x1 = []
        x2 = []
        for i in xrange(max(len(X1), len(X2))):
            if abs(X1[i] - X2[i]) > eps:
                x1.append(X1[i])
                x2.append(X2[i])
        Nr = len(x1)
        delta = sorted([(abs(x2[i] - x1[i]), i) for i in xrange(Nr)], key=lambda x: (-x[0], x[1]))
        W = 0
        for rank in xrange(Nr):
            original_x1 = x1[delta[rank][1]]
            original_x2 = x2[delta[rank][1]]
            sign = 1
            if original_x1 > original_x2:
                sign = -1
            W += sign * (rank + 1)
        delta_W = math.sqrt(1.0 * Nr * (Nr + 1) * (2 * Nr + 1) / 6)
        self.W = W
        self.Nr = Nr
        self.z = (abs(W) - 0.5) / delta_W

    def get_W(self):
        return self.W

    def get_N(self):
        return self.Nr

    def get_result(self):
        if self.z < 1.645:
            print "Unknown"
        else:
            if self.W > 0:
                print "Feature RULES"
            else:
                print "Feature SUCKS"

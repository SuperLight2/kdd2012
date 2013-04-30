from feature_calcer import FeatureCalcer
from readers import InstanceReader

import logging
_logger = logging.getLogger(__name__)


class FeatureCalcerMeanCtr(FeatureCalcer):
    def calc_statistics(self):
        self.userID2ctr = {}
        self.adID2ctr = {}
        for instance in InstanceReader().open(self.training_filepath):
            if instance.userID not in self.userID2ctr:
                self.userID2ctr[instance.userID] = [0, 0]
            self.userID2ctr[instance.userID][0] += instance.clicks
            self.userID2ctr[instance.userID][1] += instance.impressions
            if instance.adID not in self.adID2ctr:
                self.adID2ctr[instance.adID] = [0, 0]
            self.adID2ctr[instance.adID][0] += instance.clicks
            self.adID2ctr[instance.adID][1] += instance.impressions

    def calc_ctr(self, clicks, impressions):
        return 0 if clicks == 0 else 1.0 * clicks / impressions

    def calc_features(self, instance):
        results = []

        if instance.userID not in self.userID2ctr:
            self.userID2ctr[instance.userID] = [0, 0]
        results.append(self.calc_ctr(self.userID2ctr[instance.userID][0], self.userID2ctr[instance.userID][1]))

        if instance.adID not in self.adID2ctr:
            self.adID2ctr[instance.adID] = [0, 0]
        results.append(self.calc_ctr(self.adID2ctr[instance.adID][0], self.adID2ctr[instance.adID][1]))

        return results
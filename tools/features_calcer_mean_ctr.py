from feature_calcer import FeatureCalcer
from readers import InstanceReader
from tools import gcd

import logging
_logger = logging.getLogger(__name__)


def depth_position_attribute(depth, position):
    g = gcd(depth - position, position)
    return (depth - position) / g, position / g


class FeatureCalcerMeanCtr(FeatureCalcer):
    ATTRIBUTES = ["userID", "adID", "advertiserID", "depth", "position", "queryID", "keywordID", "titleID",
                  "descriptionID", "userID", "user_gender", "user_age"]
    FUNCTIONS = [(attribute, lambda instance, attr: getattr(instance, attr)) for attribute in ATTRIBUTES]
    FUNCTIONS.append(("depth-position", lambda instance, _: depth_position_attribute(instance.depth, instance.position)))

    def calc_statistics(self):
        all_clicks = 0
        all_impressions = 0
        self.attr2ctr = {}

        for instance in InstanceReader().open(self.training_filepath):
            all_clicks += instance.clicks
            all_impressions += instance.impressions

            for attribute, function in FeatureCalcerMeanCtr.FUNCTIONS:
                if attribute not in self.attr2ctr:
                    self.attr2ctr[attribute] = {}

                attribute_value = function(instance, attribute)
                if attribute_value not in self.attr2ctr[attribute]:
                    self.attr2ctr[attribute][attribute_value] = [0, 0]
                self.attr2ctr[attribute][attribute_value][0] += instance.clicks
                self.attr2ctr[attribute][attribute_value][1] += instance.impressions
        self.mean_ctr = 1.0 * all_clicks / all_impressions

    def calc_ctr(self, clicks, impressions, a=0, b=0):
        return self.mean_ctr if (impressions + b) == 0 else 1.0 * (clicks + a * b) / (impressions + b)

    def calc_features(self, instance):
        """
        userID categorical ctr
        userID categorical ctr for a=0.08 b=75
        adID categorical ctr
        adID categorical ctr for a=0.08 b=75
        advertiserID categorical ctr
        advertiserID categorical ctr for a=0.08 b=75
        depth categorical ctr
        depth categorical ctr for a=0.08 b=75
        position categorical ctr
        position categorical ctr for a=0.08 b=75
        queryID categorical ctr
        queryID categorical ctr for a=0.08 b=75
        keywordID categorical ctr
        keywordID categorical ctr for a=0.08 b=75
        titleID categorical ctr
        titleID categorical ctr for a=0.08 b=75
        descriptionID categorical ctr
        descriptionID categorical ctr for a=0.08 b=75
        userID categorical ctr
        userID categorical ctr for a=0.08 b=75
        user_gender categorical ctr
        user_gender categorical ctr for a=0.08 b=75
        user_age categorical ctr
        user_age categorical ctr for a=0.08 b=75
        depth-position categorical ctr
        depth-position categorical ctr for a=0.08 b=75
        """
        results = []

        for attribute, function in FeatureCalcerMeanCtr.FUNCTIONS:
            attribute_value = function(instance, attribute)
            if attribute_value not in self.attr2ctr[attribute]:
                results.append(self.mean_ctr)
                results.append(self.mean_ctr)
                continue
            clicks, impressions = self.attr2ctr[attribute][attribute_value]
            results.append(self.calc_ctr(clicks, impressions))
            results.append(self.calc_ctr(clicks, impressions, 0.05, 75))
        return results
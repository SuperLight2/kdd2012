from feature_calcer import FeatureCalcer
from readers import InstanceReader

import logging
_logger = logging.getLogger(__name__)


class FeatureCalcerMeanCtr(FeatureCalcer):
    ATTRIBUTES = ["userID", "adID", "advertiserID", "depth", "position", "queryID", "keywordID", "titleID",
                  "descriptionID", "userID", "user_gender", "user_age"]

    def calc_statistics(self):
        all_clicks = 0
        all_impressions = 0
        self.attr2ctr = {}

        for instance in InstanceReader().open(self.training_filepath):
            all_clicks += instance.clicks
            all_impressions += instance.impressions

            for attribute in FeatureCalcerMeanCtr.ATTRIBUTES:
                if attribute not in self.attr2ctr:
                    self.attr2ctr[attribute] = {}

                attribute_value = getattr(instance, attribute)
                if attribute_value not in self.attr2ctr[attribute]:
                    self.attr2ctr[attribute][attribute_value] = [0, 0]
                self.attr2ctr[attribute][attribute_value][0] += instance.clicks
                self.attr2ctr[attribute][attribute_value][1] += instance.impressions
        self.mean_ctr = 1.0 * all_clicks / all_impressions

    def calc_ctr(self, clicks, impressions, a=0, b=0):
        return self.mean_ctr if (impressions + b) == 0 else 1.0 * (clicks + a * b) / (impressions + b)

    def calc_features(self, instance):
        results = []

        for attribute in FeatureCalcerMeanCtr.ATTRIBUTES:
            attribute_value = getattr(instance, attribute)
            if attribute_value not in self.attr2ctr[attribute]:
                results.append(self.mean_ctr)
                results.append(self.mean_ctr)
                continue
            clicks = self.attr2ctr[attribute][attribute_value][0]
            impressions = self.attr2ctr[attribute][attribute_value][1]
            results.append(self.calc_ctr(clicks, impressions))
            results.append(self.calc_ctr(clicks, impressions, 0.05, 75))
        return results
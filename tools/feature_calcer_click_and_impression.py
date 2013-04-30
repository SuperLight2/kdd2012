from feature_calcer import FeatureCalcer

import logging
_logger = logging.getLogger(__name__)


class FeatureCalcerClickAndImpression(FeatureCalcer):
    def calc_statistics(self):
        pass

    def calc_features(self, instance):
        if instance.clicks == 0:
            return 0
        else:
            return 1.0 * instance.clicks / instance.impressions
from feature_calcer import FeatureCalcer


class FeatureCalcerGeneral(FeatureCalcer):
    def calc_statistics(self):
        pass

    def calc_features(self, instance):
        return [
            instance.adID, instance.advertiserID,
            instance.queryID, len(instance.query_tokens),
            instance.keywordID, len(instance.keyword_tokens),
            instance.titleID, len(instance.title_tokens),
            instance.descriptionID, len(instance.description_tokens),
            instance.userID, instance.user_age, instance.user_gender,
            instance.position, instance.depth,
            1.0 * instance.position / instance.depth,
            1.0 * (instance.position + 0.5 * 0.8) / (instance.depth + 0.5),
            int(instance.adID) / 1000,
            int(instance.advertiserID) / 1000,
            int(instance.queryID) / 1000,
            int(instance.keywordID) / 1000,
            int(instance.titleID) / 1000,
            int(instance.descriptionID) / 1000,
            int(instance.userID) / 1000]
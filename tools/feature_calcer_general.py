from feature_calcer import FeatureCalcer


class FeatureCalcerGeneral(FeatureCalcer):
    def calc_statistics(self):
        pass

    def calc_features(self, instance):
        """
        adID
        advertiserID
        queryID
        len(instance.query_tokens)
        instance.keywordID
        len(instance.keyword_tokens)
        instance.titleID
        len(instance.title_tokens)
        instance.descriptionID
        len(instance.description_tokens)
        instance.userID
        instance.user_age
        instance.user_gender
        instance.position
        instance.depth
        1.0 * instance.position / instance.depth
        int(instance.adID) / 2300
        int(instance.advertiserID) / 4
        int(instance.queryID) / 2600
        int(instance.keywordID) / 125
        int(instance.titleID) / 400
        int(instance.descriptionID) / 320
        int(instance.userID) / 2400
        """
        return [
            instance.adID,
            instance.advertiserID,
            instance.queryID,
            len(instance.query_tokens),
            instance.keywordID,
            len(instance.keyword_tokens),
            instance.titleID,
            len(instance.title_tokens),
            instance.descriptionID,
            len(instance.description_tokens),
            instance.userID,
            instance.user_age,
            instance.user_gender,
            instance.position,
            instance.depth,
            1.0 * instance.position / instance.depth,
            int(instance.adID) / 2300,
            int(instance.advertiserID) / 4,
            int(instance.queryID) / 2600,
            int(instance.keywordID) / 125,
            int(instance.titleID) / 400,
            int(instance.descriptionID) / 320,
            int(instance.userID) / 2400]
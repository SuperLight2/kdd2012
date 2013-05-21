import math


class IMetric:
    def __init__(self):
        self.summator = 0
        self.elements_count = 0

    def add(self, original_class, class_probabilities):
        raise BaseException("Unimplemented exception")

    def get_result(self):
        raise BaseException("Unimplemented exception")


class MulticlassLogloss(IMetric):
    def add(self, original_class, class_probabilities):
        self.elements_count += 1
        p = 0
        if original_class in class_probabilities:
            p = class_probabilities[original_class]
        p = max(min(p, 1 - 1e-15), 1e-15)
        self.summator -= math.log(p)

    def get_result(self):
        return 1.0 * self.summator / self.elements_count


class RightClassificationRatio(IMetric):
    def add(self, original_class, class_probabilities):
        self.elements_count += 1
        original_class_probability = 0
        if original_class in class_probabilities:
            original_class_probability = class_probabilities[original_class]
        for key, value in class_probabilities.iteritems():
            if key != original_class:
                if value > original_class_probability:
                    return
        self.summator += 1

    def get_result(self):
        return 1.0 * self.summator / self.elements_count


class MSE(IMetric):
    def add(self, original_value, value):
        self.elements_count += 1
        try:
            self.summator += (float(original_value) - value) ** 2
        except ValueError:
            pass

    def get_result(self):
        return 1.0 * self.summator / self.elements_count


class AUC:
    def __init__(self):
        self.elements_count = 0
        self.num_clicks = []
        self.num_impressions = []
        self.predicted_ctr = []

    def add(self, clicks, impressions, predicted_ctr):
        try:
            float(clicks)
            float(impressions)
            float(predicted_ctr)
        except ValueError:
            return
        self.elements_count += 1
        self.num_clicks.append(float(clicks))
        self.num_impressions.append(float(impressions))
        self.predicted_ctr.append(float(predicted_ctr))

    def get_result(self):
        if not self.elements_count:
            return 0

        i_sorted = sorted(range(len(self.predicted_ctr)), key=lambda i: self.predicted_ctr[i], reverse=True)
        auc_temp = 0.0
        click_sum = 0.0
        old_click_sum = 0.0
        no_click = 0.0
        no_click_sum = 0.0

        # treat all instances with the same predicted_ctr as coming from the
        # same bucket
        last_ctr = self.predicted_ctr[i_sorted[0]] + 1.0

        for i in xrange(len(self.predicted_ctr)):
            if last_ctr != self.predicted_ctr[i_sorted[i]]:
                auc_temp += (click_sum + old_click_sum) * no_click / 2.0
                old_click_sum = click_sum
                no_click = 0.0
                last_ctr = self.predicted_ctr[i_sorted[i]]
            no_click += self.num_impressions[i_sorted[i]] - self.num_clicks[i_sorted[i]]
            no_click_sum += self.num_impressions[i_sorted[i]] - self.num_clicks[i_sorted[i]]
            click_sum += self.num_clicks[i_sorted[i]]
        auc_temp += (click_sum + old_click_sum) * no_click / 2.0
        auc = auc_temp / (click_sum * no_click_sum + 1e-15)
        return auc

import math


class GiniFunction:
    @staticmethod
    def calc(classes_count):
        total = 0
        for values in classes_count.values():
            total += values
        result = 1
        for class_count in classes_count.values():
            result -= (1.0 * class_count / total) ** 2
        return result


class EntropyFunction:
    @staticmethod
    def calc(classes_count):
        total = 0
        for values in classes_count.values():
            total += values
        result = 0
        for class_count in classes_count.values():
            p = 1.0 * class_count / total
            if abs(p) > 1e-15:
                result -= p * math.log(p)
        return result
import math


class Histogram(object):
    def __init__(self, bins_count=None, values=None):
        self.histogram = dict()
        if values is not None:
            for key in values:
                self.histogram[key] = 1
        self.bins_count = len(self.histogram)
        if bins_count is not None:
            self.bins_count = bins_count
        self.normalize()

    def __str__(self):
        keys = sorted(self.histogram.keys(), key=lambda x: float(x))
        return "\t".join([str(key) + ":" + str(self.histogram[key]) for key in keys])

    def __eq__(self, other):
        return self.histogram == other.histogram

    def add(self, key, value=1):
        if key not in self.histogram:
            self.histogram[key] = 0
        self.histogram[key] += value
        self.normalize()

    def merge(self, histogram):
        for key, value in histogram.histogram.iteritems():
            if key not in self.histogram:
                self.histogram[key] = 0
            self.histogram[key] += value
        self.normalize()

    def sum(self, a):
        plain = sorted([(key, value) for key, value in self.histogram.iteritems()], key=lambda x: float(x[0]))
        if a < plain[0][0]:
            return 0
        if a > plain[-1][0]:
            result = 0
            for key, value in plain:
                result += value
            return result
        result = 0
        for i in xrange(len(plain) - 1):
            if (plain[i][0] <= a) and (a < plain[i + 1][0]):
                m_b = plain[i][1] + 1.0 * (plain[i + 1][1] - plain[i][1]) * (a - plain[i][0]) / (plain[i + 1][0] - plain[i][0])
                result += 1.0 * (plain[i][1] + m_b) * (a - plain[i][0]) / (plain[i + 1][0] - plain[i][0]) / 2
                result += 1.0 * plain[i][1] / 2
                break
            result += plain[i][1]
        return result

    def uniform(self, B):
        bins_sum = 0

        for value in self.histogram.values():
            bins_sum += value
        result = [0 for _ in xrange(B - 1)]
        sums = sorted([(x, self.sum(x)) for x in self.histogram.keys()], key=lambda x: float(x[0]))

        for j in xrange(B - 1):
            s = 1.0 * (j + 1) * bins_sum / B
            if s > sums[-1][1]:
                result[j] = result[j - 1]
                continue
            i = 0
            while (i < len(sums)) and (sums[i][1] < s):
                i += 1
            i -= 1
            while i + 1 >= len(self.histogram):
                i -= 1
            if i < 0:
                i = 0
            d = s - sums[i][1]
            if d < 0:
                d = 0
            a = self.histogram[sums[i + 1][0]] - self.histogram[sums[i][0]]
            b = 2 * self.histogram[sums[i][0]]
            c = -2 * d

            if abs(a) < 1e-8:
                z = 1.0 * d / self.histogram[sums[i][0]]
            else:
                z = (-b + math.sqrt(b * b - 4 * a * c)) / (2.0 * a)
            result[j] = sums[i][0] + z * (sums[i + 1][0] - sums[i][0])
        return result

    def normalize(self):
        while len(self.histogram) > self.bins_count:
            keys = sorted(self.histogram.keys(), key=lambda x: float(x))
            min_difference_index = 0
            min_difference = keys[min_difference_index + 1] - keys[min_difference_index]
            for i in xrange(len(keys) - 1):
                if min_difference > keys[i + 1] - keys[i]:
                    min_difference_index = i
                    min_difference = keys[i + 1] - keys[i]
            q_i = keys[min_difference_index]
            q_i_plus_one = keys[min_difference_index + 1]
            k_i = self.histogram[q_i]
            k_i_plus_one = self.histogram[q_i_plus_one]
            del(self.histogram[q_i])
            del(self.histogram[q_i_plus_one])
            self.histogram[1.0 * (q_i * k_i + q_i_plus_one * k_i_plus_one) / (k_i + k_i_plus_one)] = k_i + k_i_plus_one


if __name__ == '__main__':
    hist1 = Histogram(values=[23, 19, 10, 16, 36])
    hist2 = Histogram(values=[32, 30, 45])
    print hist1
    print hist2
    hist1.add(2)
    print hist1
    hist1.add(9)
    print hist1
    hist1.merge(hist2)
    print hist1
    print hist1.sum(15)
    hist3 = Histogram(values=[23, 19, 10, 16, 36, 32, 30, 45])
    print hist1.uniform(3)
    print hist1.sum(15.21)
    print hist1.sum(28.98) - hist1.sum(15.21)
    print hist3.sum(15.21)
    print hist3.sum(28.98) - hist3.sum(15.21)
    print hist1.sum(1000)




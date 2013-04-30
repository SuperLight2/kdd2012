from smart_writer import SmartWriter
from smart_reader import SmartReader
from types import ListType


class FeatureCalcer(object):
    def __init__(self, training_filepath, test_filepath, result_training, result_test):
        self.training_filepath = training_filepath
        self.test_filepath = test_filepath
        self.result_training = result_training
        self.result_test = result_test

    def calc_statistics(self):
        raise BaseException("Unimplemented statistics function")

    def calc_features(self, instance):
        raise BaseException("Unimplemented features function")

    def run(self):
        self.calc_statistics()
        for in_filepath, out_filepath in zip([self.training_filepath, self.test_filepath], [self.result_training, self.result_test]):
            with SmartWriter().open(out_filepath) as f_out:
                for instance in SmartReader().open(in_filepath):
                    result = self.calc_features(instance)
                    if not isinstance(result, ListType):
                        result = [result]
                    print >> f_out, "\t".join(map(str, result))

import os
import unittest

from django_behave import runner


os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'localhost:9090'


class AcceptanceTestSuiteRunner(runner.BaseRunner):
    (option_list, option_info) = runner.get_options()

    def make_bdd_test_suite(self, features_dir):
        return runner.DjangoBehaveTestCase(features_dir=features_dir,
                                           option_info=self.option_info)

    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        #test_labels = ["bericht.apps.%s" % l for l in test_labels]
        suite_without_unittests = unittest.TestSuite()
        for label in test_labels:
            app = runner.get_app(label)
            features_dir = runner.get_features(app)
            if features_dir is not None:
                test = self.make_bdd_test_suite(features_dir)
                suite_without_unittests.addTest(test)

        return suite_without_unittests

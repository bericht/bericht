import unittest

from django_behave import runner


class AcceptanceTestSuiteRunner(runner.DjangoBehaveTestSuiteRunner):
    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        suite = super(self.__class__, self).build_suite(
            test_labels, extra_tests, **kwargs)
        suite_without_unittests = unittest.TestSuite()

        for test_case in suite:
            if isinstance(test_case, runner.DjangoBehaveTestCase):
                suite_without_unittests.addTest(test_case)

        return suite_without_unittests

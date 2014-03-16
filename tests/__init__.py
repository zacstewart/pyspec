from pyspec import *
from unittest import TestCase
from mock import Mock, call


class SuiteTest(TestCase):

    def test_report_success(self):
        out = Mock()
        suite = Suite(out=out)
        suite.report_success(Mock())
        out.write.assert_called_with('.')

    def test_report_failure(self):
        out = Mock()
        suite = Suite(out=out)

        suite.report_failure(
            Mock(scenario_description='Foo bar'),
            AssertionError('Miserable failure'))
        out.write.assert_called_with('F')

        suite.report_results()
        out.write.assert_any_call('1 failures, 0 errors\n')
        out.write.assert_any_call('Foo bar\n')
        out.write.assert_any_call('Miserable failure\n')

    def test_report_error(self):
        out = Mock()
        suite = Suite(out=out)

        suite.report_error(
            Mock(scenario_description='Foo bar'),
            Exception('Miserable error'))
        out.write.assert_called_with('E')

        suite.report_results()
        out.write.assert_any_call('0 failures, 1 errors\n')
        out.write.assert_any_call('Foo bar\n')
        out.write.assert_any_call('Miserable error\n')

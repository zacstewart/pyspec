from pyspec import Suite, Context, context, specification
from unittest import TestCase
from mock import Mock, patch


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

    def test_is_green_after_reporting_a_success(self):
        out = Mock()
        suite = Suite(out=out)
        suite.report_success(Mock())
        self.assertTrue(suite.is_green())

    def test_is_green_after_reporting_a_failure(self):
        out = Mock()
        suite = Suite(out=out)
        suite.report_failure(Mock(), Mock())
        self.assertFalse(suite.is_green())

    def test_is_green_after_reporting_an_error(self):
        out = Mock()
        suite = Suite(out=out)
        suite.report_error(Mock(), Mock())
        self.assertFalse(suite.is_green())

    def test_is_green_after_reporting_failures_errors_and_success(self):
        out = Mock()
        suite = Suite(out=out)
        suite.report_failure(Mock(), Mock())
        suite.report_error(Mock(), Mock())
        suite.report_success(Mock())
        self.assertFalse(suite.is_green())


class ContextTest(TestCase):

    def test_full_description_as_root_context(self):
        a_context = Context(description='Foo bar')
        self.assertEqual('Foo bar', a_context.full_description)

    def test_full_description_as_nested_a_context(self):
        a_context = Context(description='Foo bar')
        a_context = Context(parent=a_context, description='baz qux')
        self.assertEqual('Foo bar baz qux', a_context.full_description)


class contextTest(TestCase):

    def test_it_pushes_into_a_nested_context_and_then_pops_back_out(self):
        with patch('pyspec.suite') as suite_handler:
            suite_handler.context = Context(None, 'Root context')
            within_context = None
            with context('foo bar'):
                within_context = suite_handler.context

            self.assertEqual('Root context', within_context.parent.description)
            self.assertEqual('foo bar', within_context.description)

            self.assertEqual('Root context', suite_handler.context.description)


class specificationTest(TestCase):

    def test_scenario_description(self):
        a_description = None
        with patch('pyspec.suite') as suite_handler:
            suite_handler.context = Mock(full_description='After foo and bar')
            a_specification = specification('next is baz')
            a_description = a_specification.scenario_description
        self.assertEqual('After foo and bar next is baz', a_description)

    def test_reports_success_when_no_exceptions_are_raised_within_block(self):
        spec = specification('foo')
        with patch('pyspec.suite') as suite_handler:
            with spec:
                assert True
            suite_handler.report_success.assert_called_with(spec)

    def test_reports_failure_for_AssertionErrors_raised_within_block(self):
        spec = specification('foo')
        failure = AssertionError('Miserable failure')
        with patch('pyspec.suite') as suite_handler:
            with spec:
                raise failure
            suite_handler.report_failure.assert_called_with(spec, failure)

    def test_reports_error_for_Exceptions_raised_within_block(self):
        spec = specification('foo')
        error = Exception('Miserable error')
        with patch('pyspec.suite') as suite_handler:
            with spec:
                raise error
            suite_handler.report_error.assert_called_with(spec, error)

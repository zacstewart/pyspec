from mock import Mock, patch
from pyspec import runner
from unittest import TestCase
import sys


class mainTest(TestCase):

    def setUp(self):
        self.original_argv = sys.argv

    def tearDown(self):
        sys.argv = self.original_argv

    def test_main_returns_0_for_green_test_suite(self):
        with patch('pyspec.suite.out'):
            sys.argv = ['pyspec', 'tests/examples/green_spec.py']
            self.assertEqual(0, runner.main())

    def test_main_returns_1_for_red_test_suite(self):
        with patch('pyspec.suite.out'):
            sys.argv = ['pyspec', 'tests/examples/red_spec.py']
            self.assertEqual(1, runner.main())

    def test_main_returns_1_for_broken_test_suite(self):
        with patch('pyspec.suite.out'):
            sys.argv = ['pyspec', 'tests/examples/broken_spec.py']
            self.assertEqual(1, runner.main())

    def test_main_returns_1_for_non_existent_test_suite(self):
        with patch('pyspec.suite.out'):
            sys.argv = ['pyspec', 'tests/examples/non_existent_spec.py']
            self.assertEqual(1, runner.main())

    def test_main_runs_entire_directory_of_specs(self):
        with patch('pyspec.suite') as suite_handler:
            suite_handler.out = Mock()
            sys.argv = ['pyspec', 'tests/examples']
            runner.main()
            self.assertTrue(suite_handler.report_success.called)
            self.assertTrue(suite_handler.report_failure.called)
            self.assertTrue(suite_handler.report_error.called)

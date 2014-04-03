from pyspec.expectations import ExpectationNotMetError, EqualityMatcher, \
    PositiveHandler, NegativeHandler, Target
from unittest import TestCase
from mock import Mock, patch


class ExpectationNotMetErrorTest(TestCase):

    def setUp(self):
        self.error = ExpectationNotMetError('foo')

    def test_string_conversion(self):
        self.assertEqual('foo', str(self.error))


class PositiveHandlerTest(TestCase):

    def test_resolve_with_a_matching_matcher(self):
        matcher = EqualityMatcher('foo')
        handler = PositiveHandler('foo', matcher)
        handler.resolve()

    def test_resolve_with_a_non_matching_matcher(self):
        matcher = EqualityMatcher('bar')
        handler = PositiveHandler('foo', matcher)
        self.assertRaises(ExpectationNotMetError, handler.resolve)


class NegativeHandlerTest(TestCase):

    def test_resolve_with_a_matching_matcher(self):
        matcher = EqualityMatcher('foo')
        handler = NegativeHandler('foo', matcher)
        self.assertRaises(ExpectationNotMetError, handler.resolve)

    def test_resolve_with_a_non_matching_matcher(self):
        pass


class TargetTest(TestCase):

    def setUp(self):
        self.target = Target('foo')

    def test_to(self):
        with patch('pyspec.expectations.PositiveHandler') as handler:
            matcher = Mock()
            instance = handler.return_value

            self.target.to(matcher)

            handler.assert_called_with('foo', matcher)
            instance.resolve.assert_called_with()

    def test_not_to(self):
        with patch('pyspec.expectations.NegativeHandler') as handler:
            matcher = Mock()
            instance = handler.return_value

            self.target.not_to(matcher)

            handler.assert_called_with('foo', matcher)
            self.target.not_to(Mock())
            instance.resolve.assert_called_with()

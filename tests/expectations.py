from pyspec.expectations import *
from unittest import TestCase
from mock import Mock, patch


class ExpectationNotMetErrorTest(TestCase):

    def setUp(self):
        self.error = ExpectationNotMetError('foo')

    def test_string_conversion(self):
        self.assertEqual('foo', str(self.error))


class EqualityMatcherTest(TestCase):

    def setUp(self):
        self.matcher = EqualityMatcher('foo')

    def test_matches_with_an_equal_value(self):
        self.assertTrue(self.matcher.matches('foo'))
        self.assertEqual(
            'Expected foo not to be equal to foo',
            self.matcher.failure_message_when_negated)

    def test_matches_with_an_inequal_value(self):
        self.assertFalse(self.matcher.matches('bar'))
        self.assertEqual(
            'Expected bar to be equal to foo',
            self.matcher.failure_message)


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


class ExpecationsIntegrationTest(TestCase):

    def test_expect_equal_with_equal_value(self):
        expect(1).to(eq(1))

    def test_expect_not_equal_with_equal_value(self):
        self.assertRaises(ExpectationNotMetError, expect(1).not_to, eq(1))

    def test_expect_equal_with_inequal_value(self):
        self.assertRaises(ExpectationNotMetError, expect(1).to, eq(2))

    def test_expect_not_equal_with_inequal_value(self):
        expect(1).not_to(eq(2))

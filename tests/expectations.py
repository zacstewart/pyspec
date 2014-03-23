from pyspec.expectations import *
from unittest import TestCase
from mock import Mock, patch


class ExpectationNotMetErrorTest(TestCase):

    def setUp(self):
        self.error = ExpectationNotMetError('foo')

    def test_string_conversion(self):
        self.assertEqual('foo', str(self.error))


class MatcherTest(TestCase):

    def setUp(self):
        self.matcher = Matcher('foo')

    def test_matches(self):
        self.assertRaises(NotImplementedError, self.matcher.matches, 'bar')
        self.assertRaises(NotImplementedError, self.matcher.failure_message)
        self.assertRaises(NotImplementedError,
                          self.matcher.failure_message_when_negated)


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


class IdentityMatcherTest(TestCase):

    def setUp(self):
        self.matcher = IdentityMatcher(None)

    def test_matches_with_an_identical_object(self):
        self.assertTrue(self.matcher.matches(None))
        self.assertEqual(
            'Expected None not to be None',
            self.matcher.failure_message_when_negated)

    def test_matches_with_an_inequal_value(self):
        self.assertFalse(self.matcher.matches(False))
        self.assertEqual(
            'Expected False to be None',
            self.matcher.failure_message)


class GreaterThanMatcherTest(TestCase):

    def setUp(self):
        self.matcher = GreaterThanMatcher(1)

    def test_matches_with_a_greater_actual(self):
        self.assertTrue(self.matcher.matches(2))
        self.assertEqual(
            'Expected 2 not to be > 1',
            self.matcher.failure_message_when_negated)

    def test_matches_with_a_lesser_actual(self):
        self.assertFalse(self.matcher.matches(0))
        self.assertEqual(
            'Expected 0 to be > 1',
            self.matcher.failure_message)


class LessThanMatcherTest(TestCase):

    def setUp(self):
        self.matcher = LessThanMatcher(1)

    def test_matches_with_a_greater_actual(self):
        self.assertTrue(self.matcher.matches(0))
        self.assertEqual(
            'Expected 0 not to be < 1',
            self.matcher.failure_message_when_negated)

    def test_matches_with_a_lesser_actual(self):
        self.assertFalse(self.matcher.matches(2))
        self.assertEqual(
            'Expected 2 to be < 1',
            self.matcher.failure_message)


class GreaterThanMatcherOrEqualTest(TestCase):

    def setUp(self):
        self.matcher = GreaterThanOrEqualMatcher(1)

    def test_matches_with_a_greater_actual(self):
        self.assertTrue(self.matcher.matches(2))
        self.assertEqual(
            'Expected 2 not to be >= 1',
            self.matcher.failure_message_when_negated)

    def test_matches_with_a_lesser_actual(self):
        self.assertFalse(self.matcher.matches(0))
        self.assertEqual(
            'Expected 0 to be >= 1',
            self.matcher.failure_message)

    def test_matches_with_an_equal_actual(self):
        self.assertTrue(self.matcher.matches(1))
        self.assertEqual(
            'Expected 1 not to be >= 1',
            self.matcher.failure_message_when_negated)


class LessThanOrEqualMatcherTest(TestCase):

    def setUp(self):
        self.matcher = LessThanOrEqualMatcher(1)

    def test_matches_with_a_greater_actual(self):
        self.assertTrue(self.matcher.matches(0))
        self.assertEqual(
            'Expected 0 not to be <= 1',
            self.matcher.failure_message_when_negated)

    def test_matches_with_a_lesser_actual(self):
        self.assertFalse(self.matcher.matches(2))
        self.assertEqual(
            'Expected 2 to be <= 1',
            self.matcher.failure_message)

    def test_matches_with_an_equal_actual(self):
        self.assertTrue(self.matcher.matches(1))
        self.assertEqual(
            'Expected 1 not to be <= 1',
            self.matcher.failure_message_when_negated)


class WithinDeltaMatcherTest(TestCase):

    def setUp(self):
        self.matcher = WithinDeltaMatcher(3)

    def test_of_0_with_1(self):
        self.assertTrue(self.matcher.of(0).matches(1))
        self.assertEqual('Expected 1 not to be within 3 of 0',
                         self.matcher.failure_message_when_negated)

    def test_of_0_with_negative_1(self):
        self.assertTrue(self.matcher.of(0).matches(-1))
        self.assertEqual('Expected -1 not to be within 3 of 0',
                         self.matcher.failure_message_when_negated)

    def test_of_0_with_4(self):
        self.assertFalse(self.matcher.of(0).matches(4))
        self.assertEqual('Expected 4 to be within 3 of 0',
                         self.matcher.failure_message)

    def test_of_0_with_negative_4(self):
        self.assertFalse(self.matcher.of(0).matches(-4))
        self.assertEqual('Expected -4 to be within 3 of 0',
                         self.matcher.failure_message)


class RegexMatcherTest(TestCase):

    def setUp(self):
        self.matcher = RegexMatcher('^[a-z]{6}$')

    def test_match_foobar(self):
        self.assertTrue(self.matcher.matches('foobar'))
        self.assertEqual('Expected foobar not to match ^[a-z]{6}$',
                         self.matcher.failure_message_when_negated)

    def test_match_symbols(self):
        self.assertFalse(self.matcher.matches('#$@#!'))
        self.assertEqual('Expected #$@#! to match ^[a-z]{6}$',
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

    def test_expect_to_be_with_identical_object(self):
        obj = object()
        same_obj = obj
        expect(obj).to(be(same_obj))

    def test_expect_not_to_be_with_identical_object(self):
        obj = object()
        same_obj = obj
        self.assertRaises(ExpectationNotMetError,
                          expect(obj).not_to, be(same_obj))

    def test_expect_to_be_with_non_identical_object(self):
        obj = object()
        other_obj = object()
        self.assertRaises(ExpectationNotMetError,
                          expect(obj).to, be(other_obj))

    def test_expect_not_to_be_with_non_identical_object(self):
        obj = object()
        other_obj = object()
        expect(obj).not_to(be(other_obj))

    def test_greater_than_with_greater_value(self):
        expect(2).to(be_gt(1))

    def test_greater_than_with_lesser_value(self):
        self.assertRaises(ExpectationNotMetError, expect(0).to, be_gt(1))

    def test_not_greater_than_with_greater_value(self):
        self.assertRaises(ExpectationNotMetError, expect(2).not_to, be_gt(1))

    def test_not_greater_than_with_lesser_value(self):
        expect(0).not_to(be_gt(1))

    def test_less_than_with_greater_value(self):
        expect(1).to(be_lt(2))

    def test_less_than_with_lesser_value(self):
        self.assertRaises(ExpectationNotMetError, expect(1).to, be_lt(0))

    def test_not_less_than_with_greater_value(self):
        self.assertRaises(ExpectationNotMetError, expect(1).not_to, be_lt(2))

    def test_not_less_than_with_lesser_value(self):
        expect(1).not_to(be_lt(0))

    def test_greater_than_or_equal_with_lesser_value(self):
        expect(2).to(be_gte(1))

    def test_less_than_or_equal_with_greater_value(self):
        expect(1).to(be_lte(2))

    def test_be_within_3_of_0(self):
        expect(2).to(be_within(3).of(0))

    def test_expect_string_to_match_pattern(self):
        expect('foobar').to(match(r'^[a-z]{6}$'))

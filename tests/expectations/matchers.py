from pyspec.expectations import ExpectationNotMetError
from pyspec.expectations import Matcher, EqualityMatcher, IdentityMatcher, \
    GreaterThanMatcher, LessThanMatcher, GreaterThanOrEqualMatcher, \
    LessThanOrEqualMatcher, WithinDeltaMatcher, RegexMatcher, \
    InstanceOfMatcher, OfTypeMatcher, InclusionMatcher, TruthyMatcher, \
    FalsyMatcher, RaiseErrorMatcher
from pyspec.expectations import expect, eq, be, be_gt, be_lt, be_gte, be_lte, \
    be_within, match, be_an_instance_of, be_of_type, include, be_truthy, \
    be_falsy, raise_error
from unittest import TestCase


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


class InstanceOfMatcherTest(TestCase):

    class DummyString(str):
        pass

    def setUp(self):
        self.matcher = InstanceOfMatcher(str)

    def test_matches_expected_type(self):
        self.assertTrue(self.matcher.matches('foobar'))
        self.assertEqual(
            "Expected 'foobar' not to be an instance of {0}".format(str),
            self.matcher.failure_message_when_negated)

    def test_matches_subclasses_of_expected_type(self):
        self.assertTrue(self.matcher.matches(self.DummyString('foobar')))
        self.assertEqual(
            "Expected 'foobar' not to be an instance of {0}".format(str),
            self.matcher.failure_message_when_negated)

    def test_does_not_match_non_descendents(self):
        self.assertFalse(self.matcher.matches(['string', 'list']))
        self.assertEqual(
            "Expected ['string', 'list'] to be an instance "
            "of {0}, not {1}".format(str, list),
            self.matcher.failure_message)


class OfTypeMatcherTest(TestCase):

    class DummyString(str):
        pass

    def setUp(self):
        self.matcher = OfTypeMatcher(str)

    def test_matches_an_instance_of_actual(self):
        self.assertTrue(self.matcher.matches('foobar'))
        self.assertEqual(
            "Expected 'foobar' not to be of type {0}".format(str),
            self.matcher.failure_message_when_negated)

    def test_does_not_match_an_instance_of_subclass_of_actual(self):
        self.assertFalse(self.matcher.matches(self.DummyString('foobar')))
        self.assertEqual(
            "Expected 'foobar' to be of type {0}, not {1}".format(
                str, self.DummyString),
            self.matcher.failure_message)

    def test_does_not_match_an_instance_of_some_other_class(self):
        self.assertFalse(self.matcher.matches(['foobar']))
        self.assertEqual(
            "Expected ['foobar'] to be of type {0}, not {1}".format(str, list),
            self.matcher.failure_message)


class InclusionMatcherWithSetTest(TestCase):

    def setUp(self):
        self.matcher = InclusionMatcher(['foo'])

    def test_matches_a_set_including_actual(self):
        self.assertTrue(self.matcher.matches(set(['foo', 'baz'])))
        self.assertEqual(
            "Expected foo not to be in set(['foo', 'baz'])",
            self.matcher.failure_message_when_negated)

    def test_does_not_match_an_item_not_in_the_set(self):
        self.assertFalse(self.matcher.matches(set(['bar', 'baz'])))
        self.assertTrue(
            ("Expected foo to be in set(['bar', 'baz'])" ==
             self.matcher.failure_message) or
            ("Expected foo to be in set(['baz', 'bar'])" ==
             self.matcher.failure_message))


class InclusionMatcherWithList(TestCase):

    def setUp(self):
        self.matcher = InclusionMatcher(['foo'])

    def test_matches_a_list_including_actual(self):
        self.assertTrue(self.matcher.matches(['foo', 'bar']))
        self.assertEqual(
            "Expected foo not to be in ['foo', 'bar']",
            self.matcher.failure_message_when_negated)

    def test_does_not_match_an_item_not_in_the_list(self):
        self.assertFalse(self.matcher.matches(['bar', 'baz']))
        self.assertEqual(
            "Expected foo to be in ['bar', 'baz']",
            self.matcher.failure_message)

    def test_does_not_match_if_any_items_are_not_in_the_list(self):
        matcher = InclusionMatcher(['foo', 'baz'])
        self.assertFalse(matcher.matches(['foo', 'bar']))
        self.assertEqual(
            "Expected baz to be in ['foo', 'bar']",
            matcher.failure_message)


class InclusionMatcherWithString(TestCase):

    def setUp(self):
        self.matcher = InclusionMatcher(['foo'])

    def test_matches_a_substring(self):
        self.assertTrue(self.matcher.matches('foobar'))
        self.assertEqual(
            "Expected foo not to be in foobar",
            self.matcher.failure_message_when_negated)

    def test_does_not_match_a_non_substring(self):
        self.assertFalse(self.matcher.matches('oof'))
        self.assertEqual(
            "Expected foo to be in oof",
            self.matcher.failure_message)


class InclusionMatcherWithDict(TestCase):

    def setUp(self):
        self.matcher = InclusionMatcher(['foo'])

    def test_matches_a_dict_including_a_key_of_actual(self):
        self.assertTrue(self.matcher.matches(dict(foo='quux')))
        self.assertEqual(
            "Expected foo not to be in {'foo': 'quux'}",
            self.matcher.failure_message_when_negated)

    def test_does_not_match_an_item_not_in_the_dicts_keys(self):
        self.assertFalse(self.matcher.matches(dict(bar='baz')))
        self.assertEqual(
            "Expected foo to be in {'bar': 'baz'}",
            self.matcher.failure_message)

    def test_matches_multiple_actuals(self):
        matcher = InclusionMatcher(['foo', 'bar', 'baz'])
        self.assertTrue(matcher.matches(dict(
            foo='foo', bar='bar', baz='baz')))


class TruthyMatcherTest(TestCase):

    def setUp(self):
        self.matcher = TruthyMatcher(None)

    def test_matches_string(self):
        self.assertTrue(self.matcher.matches('foo'))
        self.assertEqual(
            "Expected 'foo' to be falsy",
            self.matcher.failure_message_when_negated)

    def test_does_not_match_empty_string(self):
        self.assertFalse(self.matcher.matches(''))
        self.assertEqual(
            "Expected '' to be truthy",
            self.matcher.failure_message)


class FalsyMatcherTest(TestCase):

    def setUp(self):
        self.matcher = FalsyMatcher(None)

    def test_matches_empty_string(self):
        self.assertTrue(self.matcher.matches(''))
        self.assertEqual(
            "Expected '' to be truthy",
            self.matcher.failure_message_when_negated)

    def test_does_not_match_string(self):
        self.assertFalse(self.matcher.matches('foo'))
        self.assertEqual(
            "Expected 'foo' to be falsy",
            self.matcher.failure_message)


class RaiseErrorMatcherTest(TestCase):

    def setUp(self):
        self.matcher = RaiseErrorMatcher(IndexError)

    def test_matchest_when_an_IndexError_is_raised(self):
        callable_actual = [].pop
        self.assertTrue(self.matcher.matches(callable_actual))
        self.assertEqual(
            "Expected {0} not to raise <type 'exceptions.IndexError'>".format(
                callable_actual),
            self.matcher.failure_message_when_negated)

    def test_does_not_match_when_no_exception_is_raised(self):
        callable_actual = [0].pop
        self.assertFalse(self.matcher.matches(callable_actual))
        self.assertEqual(
            "Expected {0} to raise <type 'exceptions.IndexError'>".format(
                callable_actual),
            self.matcher.failure_message)

    def test_does_not_match_when_a_different_exception_is_raised(self):
        callable_actual = lambda: {}['foo']
        self.assertFalse(self.matcher.matches(callable_actual))
        self.assertEqual(
            "Expected {0} to raise <type 'exceptions.IndexError'>, "
            "not <type 'exceptions.KeyError'>".format(callable_actual),
            self.matcher.failure_message)


class ExpecationsSmokeTest(TestCase):

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

    def test_expect_string_to_be_an_instance_of_str(self):
        expect('foobar').to(be_an_instance_of(str))

    def test_expect_string_be_of_type_str(self):
        expect('foobar').to(be_of_type(str))

    def test_expect_member_to_be_in_list(self):
        expect(['foo', 'bar', 'baz']).to(include('foo', 'baz'))

    def test_expect_something_not_to_be_in_list(self):
        expect(['foo', 'bar']).not_to(include('baz'))

    def test_expect_string_to_be_truthy(self):
        expect('foo').to(be_truthy())

    def test_expect_empty_string_not_to_be_truthy(self):
        expect('').not_to(be_truthy())

    def test_expect_empty_string_to_be_falsy(self):
        expect('').to(be_falsy())

    def test_expect_string_not_to_be_falsy(self):
        expect('foo').not_to(be_falsy())

    def test_expect_pop_from_empty_list_to_raise_IndexError(self):
        expect([].pop).to(raise_error(IndexError))

    def test_expect_pop_from_list_not_to_raise_IndexError(self):
        expect([0].pop).not_to(raise_error(IndexError))

    def test_expect_to_raise_error_can_take_callable_with_args(self):
        class SpecialException(Exception):
            pass

        argument = object()

        def callable_(x):
            if x is argument:
                raise SpecialException('foo')

        expect(callable_, argument).to(raise_error(SpecialException))

    def test_expect_not_to_raise_error_can_take_callable_with_args(self):
        class SpecialException(Exception):
            pass

        argument = object()

        def callable_(x):
            if not x is argument:
                raise SpecialException('foo')

        expect(callable_, argument).not_to(raise_error(SpecialException))

    def test_expect_to_raise_error_can_take_callable_with_kwargs(self):
        class SpecialException(Exception):
            pass

        argument = object()
        kwargs = dict(x=argument)

        def callable_(x=None):
            if x is argument:
                raise SpecialException('foo')

        expect(callable_, **kwargs).to(raise_error(SpecialException))

    def test_expect_not_to_raise_error_can_take_callable_with_kwargs(self):
        class SpecialException(Exception):
            pass

        argument = object()
        kwargs = dict(x=argument)

        def callable_(x=None):
            if not x is argument:
                raise SpecialException('foo')

        expect(callable_, **kwargs).not_to(raise_error(SpecialException))

    def test_expect_to_raise_error_can_take_callable_with_arg_and_kwargs(self):
        class SpecialException(Exception):
            pass

        argument = object()
        kwargs = dict(x=argument)

        def callable_(arg, x=None):
            if arg is argument and x is argument:
                raise SpecialException('foo')

        expect(callable_, argument, **kwargs).to(raise_error(SpecialException))

    def test_expect_not_to_raise_error_can_take_callable_with_arg_and_kwargs(
            self):
        class SpecialException(Exception):
            pass

        argument = object()
        kwargs = dict(x=argument)

        def callable_(arg, x=None):
            if not arg is argument or not x is argument:
                raise SpecialException('foo')

        expect(callable_, argument, **kwargs).not_to(
            raise_error(SpecialException))

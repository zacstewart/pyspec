from .matchers import *


class ExpectationNotMetError(AssertionError):
    """Represents a failed expectation."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class PositiveHandler(object):
    """Used to resolve match of *actual* against *matcher* and propogate a
    failure if it does not."""

    def __init__(self, matcher, actual, *args, **kwargs):
        self.actual = actual
        self.matcher = matcher
        self.args = args
        self.kwargs = kwargs

    def resolve(self):
        """Raises an ``ExpectationNotMetError`` error with *matcher*'s
        ``failure_message`` if *matcher* does not match *actual*."""

        if not self.matcher.matches(self.actual, *self.args, **self.kwargs):
            self.handle_failure()

    def handle_failure(self):
        raise ExpectationNotMetError(self.matcher.failure_message)


class NegativeHandler(object):
    """Used to resolve match of actual against a matcher and propogate a
    failure if it does."""

    def __init__(self, matcher, actual, *args, **kwargs):
        self.actual = actual
        self.matcher = matcher
        self.args = args
        self.kwargs = kwargs

    def resolve(self):
        """Raises an ``ExpectationNotMetError`` error with *matcher*'s
        ``failure_message_when_negated`` if *matcher* matches *actual*."""

        if self.matcher.matches(self.actual, *self.args, **self.kwargs):
            self.handle_failure()

    def handle_failure(self):
        raise ExpectationNotMetError(self.matcher.failure_message_when_negated)


class Target(object):
    """Represents a value against which expectations may be tested."""

    def __init__(self, target, *args, **kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def to(self, matcher):
        """Checks the positive case of an expectation being met."""

        PositiveHandler(
            matcher, self.target, *self.args, **self.kwargs).resolve()

    def not_to(self, matcher):
        """Checks the negative case of an expectation being met."""

        NegativeHandler(
            matcher, self.target, *self.args, **self.kwargs).resolve()


def expect(target, *args, **kwargs):
    """Returns a :class:`Target` to test expectations against."""

    return Target(target, *args, **kwargs)


def eq(expected):
    """Tests equality of expected and actual."""

    return EqualityMatcher(expected)


def be(expected):
    """Tests identify of expected and actual."""

    return IdentityMatcher(expected)


def be_gt(expected):
    """Tests that *actual* is greater than *expected*"""
    return GreaterThanMatcher(expected)


def be_lt(expected):
    """Tests that *actual* is less than *expected*"""
    return LessThanMatcher(expected)


def be_gte(expected):
    """Tests that *actual* is greater than or equal to *expected*"""
    return GreaterThanOrEqualMatcher(expected)


def be_lte(expected):
    return LessThanOrEqualMatcher(expected)
    """Tests that *actual* is less than or equal to *expected*"""


def be_within(delta):
    """Tests that *actual* is within *delta* of *expected"""
    return WithinDeltaMatcher(delta)


def match(pattern):
    """Tests that *actual* matches *pattern*"""
    return RegexMatcher(pattern)


def be_an_instance_of(class_):
    """Tests that *actual* is an instance of *expected* or a descendant
    thereof"""
    return InstanceOfMatcher(class_)


def be_of_type(type_):
    """Tests that *actual* is specifically an instance of *expected*"""
    return OfTypeMatcher(type_)


def include(*expecteds):
    """Tests that *actual* is in *expected*"""
    return InclusionMatcher(expecteds)


def be_truthy():
    """Tests that *actual* is truthy"""
    return TruthyMatcher(None)


def be_falsy():
    """Tests that *actual* is falsy"""
    return FalsyMatcher(None)


def raise_error(*expecteds):
    """Tests that calling *actual* raises error"""
    return RaiseErrorMatcher(expecteds)

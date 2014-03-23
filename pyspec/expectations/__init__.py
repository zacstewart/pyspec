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

    def __init__(self, actual, matcher):
        self.actual = actual
        self.matcher = matcher

    def resolve(self):
        """Raises an ``ExpectationNotMetError`` error with *matcher*'s
        ``failure_message`` if *matcher* does not match *actual*."""

        if not self.matcher.matches(self.actual):
            self.handle_failure()

    def handle_failure(self):
        raise ExpectationNotMetError(self.matcher.failure_message)


class NegativeHandler(object):
    """Used to resolve match of actual against a matcher and propogate a
    failure if it does."""

    def __init__(self, actual, matcher):
        self.actual = actual
        self.matcher = matcher

    def resolve(self):
        """Raises an ``ExpectationNotMetError`` error with *matcher*'s
        ``failure_message_when_negated`` if *matcher* matches *actual*."""

        if self.matcher.matches(self.actual):
            self.handle_failure()

    def handle_failure(self):
        raise ExpectationNotMetError(self.matcher.failure_message_when_negated)


class Target(object):
    """Represents a value against which expectations may be tested."""

    def __init__(self, target):
        self.target = target

    def to(self, matcher):
        """Checks the positive case of an expectation being met."""

        PositiveHandler(self.target, matcher).resolve()

    def not_to(self, matcher):
        """Checks the negative case of an expectation being met."""

        NegativeHandler(self.target, matcher).resolve()


def expect(target):
    """Returns a :class:`Target` to test expectations against."""

    return Target(target)


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

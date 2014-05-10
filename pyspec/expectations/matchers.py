import re


class Matcher(object):
    """Abstract class for matchers. Must be subclassed."""

    def __init__(self, expected):
        self.expected = expected

    def matches(self, actual, *args, **kwargs):
        self.actual = actual
        return self.match(self.expected, self.actual, *args, **kwargs)

    def match(self, expected, actual):
        """Verifies match of *actual* against *expected*"""

        raise NotImplementedError('Subclasses must implement this.')

    def failure_message(self):
        """Returns an error message for when the positive case of the matcher
        is not met"""

        raise NotImplementedError('Subclasses must implement this.')

    def failure_message_when_negated(self):
        """Returns an error message for when the negative case of the matcher
        is not met"""

        raise NotImplementedError('Subclasses must implement this.')


class EqualityMatcher(Matcher):
    def match(self, expected, actual):
        return expected == actual

    @property
    def failure_message(self):
        return "Expected {0} to be equal to {1}"\
            .format(self.actual, self.expected)

    @property
    def failure_message_when_negated(self):
        return "Expected {0} not to be equal to {1}"\
            .format(self.actual, self.expected)


class IdentityMatcher(Matcher):
    def match(self, expected, actual):
        return expected is actual

    @property
    def failure_message(self):
        return "Expected {0} to be {1}".format(self.actual, self.expected)

    @property
    def failure_message_when_negated(self):
        return "Expected {0} not to be {1}".format(self.actual, self.expected)


class GreaterThanMatcher(Matcher):
    def match(self, expected, actual):
        return actual > expected

    @property
    def failure_message(self):
        return "Expected {0} to be > {1}".format(self.actual, self.expected)

    @property
    def failure_message_when_negated(self):
        return "Expected {0} not to be > {1}".format(
            self.actual, self.expected)


class LessThanMatcher(Matcher):
    def match(self, expected, actual):
        return actual < expected

    @property
    def failure_message(self):
        return "Expected {0} to be < {1}".format(self.actual, self.expected)

    @property
    def failure_message_when_negated(self):
        return "Expected {0} not to be < {1}".format(
            self.actual, self.expected)


class GreaterThanOrEqualMatcher(Matcher):
    def match(self, expected, actual):
        return actual >= expected

    @property
    def failure_message(self):
        return "Expected {0} to be >= {1}".format(self.actual, self.expected)

    @property
    def failure_message_when_negated(self):
        return "Expected {0} not to be >= {1}".format(
            self.actual, self.expected)


class LessThanOrEqualMatcher(Matcher):
    def match(self, expected, actual):
        return actual <= expected

    @property
    def failure_message(self):
        return "Expected {0} to be <= {1}".format(self.actual, self.expected)

    @property
    def failure_message_when_negated(self):
        return "Expected {0} not to be <= {1}".format(
            self.actual, self.expected)


class WithinDeltaMatcher(Matcher):
    def __init__(self, delta):
        self.delta = delta

    def of(self, expected):
        self.expected = expected
        return self

    def match(self, expected, actual):
        return expected <= actual + self.delta \
            and expected >= actual - self.delta

    @property
    def failure_message(self):
        return "Expected {0} to be within {1} of {2}".format(
            self.actual, self.delta, self.expected)

    @property
    def failure_message_when_negated(self):
        return "Expected {0} not to be within {1} of {2}".format(
            self.actual, self.delta,  self.expected)


class RegexMatcher(Matcher):
    def match(self, pattern, actual):
        return re.match(pattern, actual) is not None

    @property
    def failure_message(self):
        return "Expected {0} to match {1}".format(
            self.actual, self.expected)

    @property
    def failure_message_when_negated(self):
        return "Expected {0} not to match {1}".format(
            self.actual,  self.expected)


class InstanceOfMatcher(Matcher):
    def match(self, expected, actual):
        return isinstance(actual, expected)

    @property
    def failure_message(self):
        return "Expected {0} to be an instance of {1}, not {2}".format(
            repr(self.actual), repr(self.expected), repr(type(self.actual)))

    @property
    def failure_message_when_negated(self):
        return "Expected {0} not to be an instance of {1}".format(
            repr(self.actual), repr(self.expected))


class OfTypeMatcher(Matcher):
    def match(self, expected, actual):
        return type(actual) is expected

    @property
    def failure_message(self):
        return "Expected {0} to be of type {1}, not {2}".format(
            repr(self.actual), repr(self.expected), repr(type(self.actual)))

    @property
    def failure_message_when_negated(self):
        return "Expected {0} not to be of type {1}".format(
            repr(self.actual), repr(self.expected))


class InclusionMatcher(Matcher):
    def match(self, expecteds, actual):
        for expected in expecteds:
            if not expected in actual:
                self.missing = expected
                return False
            self.present = expected
        return True

    @property
    def failure_message(self):
        return "Expected {0} to be in {1}".format(self.missing, self.actual)

    @property
    def failure_message_when_negated(self):
        return "Expected {0} not to be in {1}".format(
            self.present, self.actual)


class TruthyMatcher(Matcher):
    def match(self, _, actual):
        return bool(actual)

    @property
    def failure_message(self):
        return "Expected {0} to be truthy".format(repr(self.actual))

    @property
    def failure_message_when_negated(self):
        return "Expected {0} to be falsy".format(repr(self.actual))


class FalsyMatcher(Matcher):
    def match(self, _, actual):
        return not bool(actual)

    @property
    def failure_message(self):
        return "Expected {0} to be falsy".format(repr(self.actual))

    @property
    def failure_message_when_negated(self):
        return "Expected {0} to be truthy".format(repr(self.actual))


class RaiseErrorMatcher(Matcher):
    def match(self, expecteds, actual, *args, **kwargs):
        self.error = None

        try:
            actual(*args, **kwargs)
        except expecteds as error:
            self.error = error
            return True
        except BaseException as error:
            self.error = error

        return False

    @property
    def failure_message(self):
        if self.error:
            return "Expected {0} to raise {1}, not {2}".format(
                self.actual, self.expected, type(self.error))
        else:
            return "Expected {0} to raise {1}".format(
                self.actual, self.expected)

    @property
    def failure_message_when_negated(self):
        return "Expected {0} not to raise {1}".format(
            self.actual, self.expected)

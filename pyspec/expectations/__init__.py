class ExpectationNotMetError(AssertionError):
    """Represents a failed expectation."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class Matcher(object):
    """Abstract class for matchers. Must be subclassed."""

    def __init__(self, expected):
        self.expected = expected

    def matches(self, actual):
        self.actual = actual
        return self.match(self.expected, self.actual)

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

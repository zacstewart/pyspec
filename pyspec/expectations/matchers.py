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

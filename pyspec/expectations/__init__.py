class ExpectationNotMetError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class Matcher(object):
    def __init__(self, expected):
        self.expected = expected

    def matches(self, actual):
        self.actual = actual
        return self.match(self.expected, self.actual)

    def match(self, expected, actual):
        raise NotImplementedError('Subclasses must implement this.')

    def failure_message(self):
        raise NotImplementedError('Subclasses must implement this.')

    def failure_message_when_negated(self):
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


class PositiveHandler(object):
    def __init__(self, actual, matcher):
        self.actual = actual
        self.matcher = matcher

    def resolve(self):
        if self.matcher.matches(self.actual):
            return
        self.handle_failure()

    def handle_failure(self):
        raise ExpectationNotMetError(self.matcher.failure_message)


class NegativeHandler(object):
    def __init__(self, actual, matcher):
        self.actual = actual
        self.matcher = matcher

    def resolve(self):
        if not self.matcher.matches(self.actual):
            return
        self.handle_failure()

    def handle_failure(self):
        raise ExpectationNotMetError(self.matcher.failure_message_when_negated)


class Target(object):
    def __init__(self, target):
        self.target = target

    def to(self, matcher):
        PositiveHandler(self.target, matcher).resolve()

    def not_to(self, matcher):
        NegativeHandler(self.target, matcher).resolve()


def expect(target):
    return Target(target)


def eq(expected):
    return EqualityMatcher(expected)

class ExpectationNotMetError(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)

class Target(object):
  def __init__(self, target):
    self.target = target

  def to(self, matcher):
    PositiveHandler(self.target, matcher).resolve()

  def not_to(self, matcher):
    NegativeHandler(self.target, matcher).resolve()

class Matcher(object):
  def __init__(self, expected):
    self.expected = expected

  def matches(self, actual):
    self.actual = actual
    return self.match(self.expected, self.actual)

class EqualityMatcher(Matcher):
  def match(self, expected, actual):
    return expected == actual

  @property
  def failure_message(self):
    return "Expected {0} to be equal to {1}".format(self.actual, self.expected)

  @property
  def failure_message_when_negated(self):
    return "Expected {0} not to be equal to {1}".format(self.actual, self.expected)

class PositiveHandler(object):
  def __init__(self, actual, matcher):
    self.actual = actual
    self.matcher = matcher

  def resolve(self):
    if self.matcher.matches(self.actual): return
    self.handle_failure()

  def handle_failure(self):
    raise ExpectationNotMetError(self.matcher.failure_message)

class NegativeHandler(object):
  def __init__(self, actual, matcher):
    self.actual = actual
    self.matcher = matcher

  def resolve(self):
    if not self.matcher.matches(self.actual): return
    self.handle_failure()

  def handle_failure(self):
    self.matcher.failure_message_when_negated
    raise ExpectationNotMetError(self.matcher.failure_message_when_negated)

def expect(target):
  return Target(target)

def eq(expected):
  return EqualityMatcher(expected)


if __name__ == '__main__':
  # All this try..except would be the internals of a hypothetical pyspec-core

  import sys

  failures = []
  try:
    expect(1).to(eq(1))
    sys.stdout.write('.')
  except ExpectationNotMetError as failure:
    failures.append(failure)
    sys.stdout.write('F')
  try:
    expect(10).to(eq(55))
    sys.stdout.write('.')
  except ExpectationNotMetError as failure:
    failures.append(failure)
    sys.stdout.write('F')
  try:
    expect(3).not_to(eq(1000))
    sys.stdout.write('.')
  except ExpectationNotMetError as failure:
    failures.append(failure)
    sys.stdout.write('F')
  try:
    expect(3).not_to(eq(3))
    sys.stdout.write('.')
  except ExpectationNotMetError as failure:
    failures.append(failure)
    sys.stdout.write('F')

  print ''
  print "\n".join(map(lambda f: f.value, failures))

import sys


class Suite(object):
    def __init__(self):
        self.context = Context()
        self.failures = []
        self.errors = []

    def report_success(self, specification):
        sys.stdout.write('.')

    def report_failure(self, specification, failure):
        self.failures.append((specification.scenario_description, failure))
        sys.stdout.write('F')

    def report_error(self, specification, error):
        self.errors.append((specification.scenario_description, error))
        sys.stdout.write('E')

    def report_results(self):
        print '\n'
        print '{0} failures, {1} errors'\
            .format(len(self.failures), len(self.errors))
        for context, error in self.failures + self.errors:
            print ''
            print context
            print error


class Context(object):
    def __init__(self, parent=None, description=__name__):
        self.parent = parent
        self.description = description

    @property
    def full_description(self):
        description = self.description
        p = self.parent
        while p:
            description = "{0} {1}".format(p.description, description)
            p = p.parent
        return description


class context(object):
    def __init__(self, description=None):
        suite.context = Context(suite.context, description)

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        suite.context = suite.context.parent
        return True


class description(context):
    pass


class specification(object):
    def __init__(self, description):
        self.description = description

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        if type is None:
            suite.report_success(self)
        elif isinstance(value, AssertionError):
            suite.report_failure(self, value)
        else:
            suite.report_error(self, value)
        return True

    @property
    def scenario_description(self):
        return "{0} {1}"\
            .format(suite.context.full_description, self.description)


suite = Suite()

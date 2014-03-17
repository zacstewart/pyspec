import sys


class Suite(object):
    def __init__(self, out=sys.stdout):
        self.context = Context()
        self.failures = []
        self.errors = []
        self.out = out

    def is_green(self):
        return len(self.failures + self.errors) == 0

    def report_success(self, specification):
        self.out.write('.')

    def report_failure(self, specification, failure):
        self.failures.append((specification.scenario_description, failure))
        self.out.write('F')

    def report_error(self, specification, error):
        self.errors.append((specification.scenario_description, error))
        self.out.write('E')

    def report_results(self):
        self.print_line('\n')
        self.print_line('{0} failures, {1} errors'
            .format(len(self.failures), len(self.errors)))
        for context, error in self.failures + self.errors:
            self.print_line('')
            self.print_line(context)
            self.print_line(error)

    def print_line(self, message=''):
        self.out.write(str(message) + '\n')


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
        self.description = description

    def __enter__(self):
        suite.context = Context(suite.context, self.description)

    def __exit__(self, type, value, traceback):
        suite.context = suite.context.parent


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


def run_spec(filename):
    exec(compile(open(filename, 'rb').read(), filename, 'exec'),
         globals(), locals())

suite = Suite()

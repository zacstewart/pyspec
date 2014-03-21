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


def run_spec(filename):
    exec(compile(open(filename, 'rb').read(), filename, 'exec'),
         globals(), locals())

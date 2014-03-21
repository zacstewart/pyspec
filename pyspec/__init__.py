from .core import Context, Suite


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


suite = Suite()

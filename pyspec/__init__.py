import sys


class World(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.context = Context()
        self.failures = []
        self.errors = []


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
        world.context = Context(world.context, description)

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        world.context = world.context.parent
        if not world.context.parent:
            print '\n'
            print '{0} failures, {1} errors'\
                .format(len(world.failures), len(world.errors))
            for context, error in world.failures + world.errors:
                print ''
                print context
                print error
            world.reset()
        return True


class description(context):
    pass


class it(object):
    def __init__(self, description):
        self.description = description

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        if type is None:
            sys.stdout.write('.')
        elif isinstance(value, AssertionError):
            world.failures.append((self.scenario_description, value))
            sys.stdout.write('F')
        else:
            world.errors.append((self.scenario_description, value))
            sys.stdout.write('E')
        return True

    @property
    def scenario_description(self):
        return "{0} {1}"\
            .format(world.context.full_description, self.description)

world = World()

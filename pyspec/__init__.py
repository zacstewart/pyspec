import sys

class World(object):
  def __init__(self):
    self.failures = []

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
    world.current_context = Context(world.current_context, description)
  def __enter__(self):
    pass

  def __exit__(self, type, value, traceback):
    world.current_context = world.current_context.parent
    if not world.current_context.parent:
      print '\n'
      print '{0} failures'.format(len(world.failures))
      for context, failure in world.failures:
        print context
        print failure
    return True

class description(context):
  pass

class it(object):
  def __init__(self, description):
    self.description = description

  def __enter__(self):
    pass

  def __exit__(self, type, value, traceback):
    if type is not None:
      world.failures.append((self.scenario_description, value))
      sys.stdout.write('F')
    else:
      sys.stdout.write('.')
    return True

  @property
  def scenario_description(self):
    return "{0} {1}".format(world.current_context.full_description, self.description)

world = World()
world.current_context = Context()

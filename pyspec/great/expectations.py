from pyspec.expectations import *

__all__ = ['expecteth', 'equal', 'be_containeth_in', 'matcheth',
           'be_liketh', 'only_be', 'includeth', 'be_real', 'be_unreal',
           'die_with', 'be', 'be_gt', 'be_lt', 'be_lte', 'be_gte']

expecteth = expect
equal = eq
be_containeth_in = be_within

matcheth = match
be_liketh = be_an_instance_of
only_be = be_of_type

includeth = include
be_real = be_truthy
be_unreal = be_falsy

die_with = raise_error

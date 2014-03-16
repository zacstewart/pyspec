from argparse import ArgumentParser
import fnmatch
import os
import pyspec


def main(argv=None, prog=None, **kwargs):
    """The console runner for PySpec"""

    parser = ArgumentParser(argv)
    parser.add_argument('spec_path',
                        help='The path to a spec or a directory of specs',
                        nargs='?',
                        default='spec')
    options = parser.parse_args()

    if os.path.isdir(options.spec_path):
        for root, dirnames, filenames in os.walk(options.spec_path):
            for filename in fnmatch.filter(filenames, '*_spec.py'):
                execfile(os.path.join(root, filename))
    elif os.path.isfile(options.spec_path):
        execfile(options.spec_path)
    else:
        print("Spec not found: {0}".format(options.spec_path))

    pyspec.suite.report_results()

    if pyspec.suite.is_green():
        return 0
    else:
        return 1

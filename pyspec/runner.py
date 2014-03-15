from argparse import ArgumentParser
from glob import glob
import re
import pyspec

PYTHON_EXTENSION = re.compile('.py$')

suite = pyspec.suite


def modulize(filename):
    return PYTHON_EXTENSION.sub('', filename)


def main(argv=None, prog=None, **kwargs):
    """The console runner for PySpec"""

    parser = ArgumentParser()
    parser.add_argument('specs_path',
                        type=str,
                        help='The path to a spec or a directory of specs')
    options = parser.parse_args()

    for path in glob(options.specs_path):
        __import__(modulize(path))

    pyspec.suite.report_results()

from argparse import ArgumentParser
from glob import glob
import pyspec


def main(argv=None, prog=None, **kwargs):
    """The console runner for PySpec"""

    parser = ArgumentParser()
    parser.add_argument('specs_path',
                        type=str,
                        help='The path to a spec or a directory of specs')
    options = parser.parse_args()

    for path in glob(options.specs_path):
        execfile(path)

    pyspec.suite.report_results()

    if pyspec.suite.is_green():
        return 0
    else:
        return 1

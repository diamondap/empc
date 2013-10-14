import sys
from os.path import realpath, abspath, join, normpath, dirname

test_dir = dirname(realpath(__file__))
code_dir = abspath(normpath(join(test_dir, '..')))
fixture_dir = abspath(join(test_dir, 'fixtures'))
sys.path.append(code_dir)


def load_fixture(filename):
    full_path = join(fixture_dir, filename)
    with open(full_path, 'r') as f:
        return f.read()

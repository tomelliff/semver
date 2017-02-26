from __future__ import print_function
import argparse
import os.path
import sys

import semantic_version

VERSION_FILE='version.py'
VERSION_TYPES = ['major', 'minor', 'patch']

def get_version():
    if os.path.isfile(VERSION_FILE):
        with open(VERSION_FILE) as version_file:
            version_line = version_file.readlines()[0]
            try:
                version = version_line.split('=')[1].strip().strip("'").strip('"')
            except IndexError:
                print('version.py should contain the following content:')
                print('__version__ = \'{some valid semantic version}\'')
                print('e.g.:')
                print('__version__ = \'0.1.0\'')
                raise
    else:
        initial_version = '0.0.0'
        version = initial_version
    return version

def increment_version(version_type):
    version_number = get_version()
    version = semantic_version.Version(version_number, partial=True)
    if version_type == 'major':
        new_version = version.next_major()
    elif version_type == 'minor':
        new_version = version.next_minor()
    elif version_type == 'patch':
        new_version = version.next_patch()
    else:
        print('Valid versions are {}, {}, {}'.format(*VERSION_TYPES))
        sys.exist(1)

    with open(VERSION_FILE, 'wb') as version_file:
        version_file.write("__version__ = '{}'\n".format(new_version))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        description='Increment the version of the project')
    parser.add_argument('version_type', choices=VERSION_TYPES,
                        nargs='?', default='minor',
                        help='Version type to increment (default: %(default)s)')
    args = parser.parse_args()

    increment_version(args.version_type)

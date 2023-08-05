import argparse
import sys
import jinja_docker_compose.jinja_docker_compose as jinja
# import jinja_docker_compose.__version__ as __version__
from jinja_docker_compose.__version__ import __version__


def filehandle_if_exists_else_none(fname):
    try:
        return open(fname, 'r')
    except FileNotFoundError:
        return None


def open_compose_file(fname):
    if not fname:
        return filehandle_if_exists_else_none('docker-compose.yaml.j2') \
            or filehandle_if_exists_else_none('docker-compose.yml.j2')
    else:
        return filehandle_if_exists_else_none(fname)


def open_dictionary_file(fname):
    if not fname:
        return filehandle_if_exists_else_none('docker-compose.dic')
    else:
        return filehandle_if_exists_else_none(fname)


def cli(argv=None):
    parser = argparse.ArgumentParser(description="jinja-docker-compose version "+__version__)
    parser.add_argument('-f', '--file', metavar='INPUT_FILE',
                        type=open_compose_file,
                        default='',
                        help='Specify the yaml file to be transformed,'
                        ' default is docker-compose.yaml.j2'
                        ' and if that does not exist'
                        ' docker-compose.yml.j2')
    parser.add_argument('-D', '--dictionary', metavar='DICTIONARY_FILE',
                        type=open_dictionary_file,
                        default='',
                        help='Specify the dictionary file to use, default is'
                        ' docker-compose.dic.')
    parser.add_argument('-o', '--output', metavar='OUTPUT_FILE',
                        type=argparse.FileType('w'),
                        default='docker-compose.yml',
                        help='Specify an alternate output compose file'
                        ' (default: docker-compose.yml)')
    parser.add_argument('-r', '--run', action='store_true',
                        help='Run docker-compose on the generated file')
    parser.add_argument('--loader', dest='fullloader', action='store_true',
                        help='Uses the FullLoader when loading the YAML,'
                        ' this enables the possible exploit that the'
                        ' FullLoader has.')
    parser.add_argument('-v', '--version', action='version',
                        version='jinja-docker-compose version '+__version__,
                        help='Show the version and exits.')

    # If we were not given the arguments (in testing) fetch them from the system
    if not argv:
        argv = sys.argv[1:]

    # parse the arguments we know and leave the rest,
    # these will be sent to docker-compose
    (args, extras) = parser.parse_known_args(argv)

    if args.file is None:
        print('Can´t open input file')
        return False

    if args.dictionary is None:
        print('Can´t open dictionary file')
        return False

    jinja.transform(args)

    #
    # Do not run docker-compose if disabled
    #
    if args.run:
        jinja.execute_docker_compose(args.output.name, extras)

    return True

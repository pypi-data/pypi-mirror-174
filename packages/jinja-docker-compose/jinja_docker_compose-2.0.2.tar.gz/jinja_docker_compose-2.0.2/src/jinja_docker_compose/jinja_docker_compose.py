from argparse import Namespace
import sys
import json
from typing import Any
import yaml
from jinja2 import Template


def transform(args: Namespace):
    #
    # Read the dictionary from file
    #
    with open(args.dictionary.name) as f:
        dic_data = f.read()
    try:
        dic = json.loads(dic_data)
    except json.decoder.JSONDecodeError:
        return 1

    #
    # Use the more secure SafeLoader if possible, see
    # https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
    #
    if not args.fullloader:
        loader: Any = yaml.SafeLoader
    else:
        loader = yaml.FullLoader

    #
    # Transform the input file acording to the dictionary
    #
    try:
        content = Template(args.file.read()).render(dic)
    except TypeError:
        return 2
    config = yaml.load(content, Loader=loader)

    if config is None:
        raise RuntimeError('Compose file is empty')

    yaml.safe_dump(config, args.output, default_flow_style=False)
    return 0


def execute_docker_compose(filename, extras):
    from compose.cli.main import main as compose_main
    sys.argv[:] = ['docker-compose', '-f', filename] + extras
    compose_main()

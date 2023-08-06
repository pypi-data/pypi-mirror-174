"""
Parameter handling from CLI
"""

# Python standard library
import argparse
import yaml
import importlib


class Arbutus:
    def __init__(self, cli_path=None, arguments=None):
        self.main_branch = argparse.ArgumentParser(arguments)
        self.parsed_args = {}
        self.breadcrumbs = ''
        self.parameters = {}

    def parse_args(self) -> dict:
        self.parsed_args = vars(self.main_branch.parse_args())
        self.__process_args__()
        return self.parsed_args

    def get_branch(self, branch_name: str) -> argparse.ArgumentParser:
        return self.__dict__[branch_name + '_branch']

    def add_branch(self, branch_name: str, node_name: str = 'main', help_text: str = None) -> argparse.ArgumentParser:
        if not self.__dict__.get(node_name + '_node'):
            self.__dict__[node_name + '_node'] = self.__dict__[node_name + '_branch'].add_subparsers(dest=node_name)
        self.__dict__[branch_name + '_branch'] = \
            self.__dict__[node_name + '_node'].add_parser(branch_name, help=help_text)
        return self.__dict__[branch_name + '_branch']

    def add_argument(self, branch: argparse.ArgumentParser, argument_name: str, **kwargs):
        if 'type' in kwargs and kwargs['type'] in ['int', 'str', 'float']:
            kwargs['type'] = eval(kwargs['type'])
        if 'action' in kwargs:
            if type(kwargs['action']) is dict:
                try:
                    module = importlib.import_module(f"{kwargs['action']['source']}")
                    kwargs['action'] = eval(f"module.{kwargs['action']['name']}")
                except KeyError:
                    raise
            elif type(kwargs['action']) is str:
                if kwargs['action'] not in ['store', 'store_const', 'store_true', 'append', 'append_const', 'count',
                                            'help', 'version']:
                    raise KeyError
            else:
                raise TypeError
        branch.add_argument(argument_name, **kwargs)

    @staticmethod
    def new_action(method):
        class NewAction(argparse.Action):
            def __call__(self, parser, namespace, values, option_string=None):
                method(parser=parser, namespace=namespace, values=values, option_string=option_string)
                setattr(namespace, self.dest, values)
        return NewAction

    def __process_args__(self) -> None:
        all_args = list(self.parsed_args.keys())
        self.breadcrumbs = '{}.{}'.format(all_args[0], all_args[1])
        for x in all_args:
            if self.parsed_args[x] in all_args:
                self.breadcrumbs += '.' + self.parsed_args[self.parsed_args[x]]
            elif x in self.breadcrumbs:
                pass
            else:
                self.parameters[x] = self.parsed_args[x]

    def from_dict(self, dict_: dict):
        for key, value in dict_.items():
            if 'branches' in value:
                for _key in value['branches']:
                    self.add_branch(_key, key)
                self.from_dict(value['branches'])
            elif 'arguments' in value:
                for _key in value['arguments']:
                    self.add_argument(self.get_branch(key), _key, **value['arguments'][_key])
            else:
                self.from_dict(value)

    def from_yaml(self, filename: str = './config/cli.yaml'):
        with open(filename, 'r') as yaml_file:
            yaml_as_dict = yaml.load(yaml_file, Loader=yaml.SafeLoader)
        self.from_dict(yaml_as_dict)

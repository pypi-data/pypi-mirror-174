"""
Parameter handling from CLI
"""

# Python standard library
import argparse


class Arbutus:
    parsed_args = {}
    breadcrumbs = ''
    parameters = {}

    def __init__(self, arguments: list = None):
        self.main_branch = argparse.ArgumentParser(arguments)

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

    def from_yaml(self, json_as_dict: dict):
        for key, value in json_as_dict.items():
            if 'branches' in value:
                for _key in value['branches']:
                    self.add_branch(_key, key)
                self.from_yaml(value['branches'])
            elif 'arguments' in value:
                for _key in value['arguments']:
                    self.get_branch(key).add_argument(_key)
            else:
                self.from_yaml(value)


if __name__ == '__main__':
    import yaml
    with open('../gxiba/cli.yaml', 'r') as cli_yaml:
        x = yaml.load(cli_yaml, Loader=yaml.SafeLoader)
    cli = Arbutus()
    cli.from_yaml(x)
    cli.parse_args()

import sys
sys.path.append('..')
from arbutus import Arbutus


@Arbutus.new_action
def sum_(*args, **kwargs):
    total = 0
    for number in kwargs['values']:
        total += number
    print(total)


@Arbutus.new_action
def mult_(*args, **kwargs):
    total = 1
    for number in kwargs['values']:
        total = total * number
    print(total)


if __name__ == '__main__':
    cli = Arbutus()
    cli.from_yaml('cli.yaml')
    cli.parse_args()
    print(cli.breadcrumbs)
    print(cli.parsed_args)

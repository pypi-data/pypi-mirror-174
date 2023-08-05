import sys
sys.path.append('.')
import arbutus


@arbutus.Arbutus.new_action
def sum_(*args, **kwargs):
    total = 0
    for number in kwargs['values']:
        total += number
    print(total)


@arbutus.Arbutus.new_action
def mult_(*args, **kwargs):
    total = 1
    for number in kwargs['values']:
        total = total * number
    print(total)


if __name__ == '__main__':
    cli = arbutus.Arbutus()
    cli.from_yaml('sample/cli.yaml')
    cli.parse_args()

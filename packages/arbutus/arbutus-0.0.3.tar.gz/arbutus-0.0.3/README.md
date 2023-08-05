<a name="readme-top"></a>

<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
</div>

<br />
<div align="center">
  <a href="https://github.com/aubravo/arbutus">
    <img src="docs/images/arbutus.png" alt="seedling" width="120" height="120">
  </a>
<h1 align="center">arbutus</h1>
  <p align="center">
        Simplification of CLI construction in Python based on argparse: just add branches and arguments. CLI construction from yaml file also available.
    <br />
    <br />
        If you are interested in participating, please feel free to contribute.
    <br />
    <br />
    <a href="https://github.com/aubravo/arbutus"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/aubravo/arbutus/issues">Report Bug</a>
    <a href="https://github.com/aubravo/arbutus/issues">Request Feature</a>
  </p>
</div>
<br />
<br />
<div align="left">

[![Python][Python.org]][Python-url]
</div>

## Contents
* [Getting Started](#getting-started)
  * [Requirements](#requirements)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)

## Getting Started

### Requirements

* Python 3.8 or above
  * argparse
  * logger

### Installation 

```commandline
pip install arbutus
```

## Usage

Once installed, the cli can be defined using a yaml file, using the keywords branches to define new branch names and 
arguments to define new arguments and it's characteristics. For example:
```yaml
main:
  branches:
    sum:
      arguments:
        integers:
          type: float
          nargs: +
          help: list of integers to sum
          action:
            name: sum_
            source: sample
    multiply:
      arguments:
        integers:
          type: float
          nargs: +
          help: list of integers to sum
          action:
            name: mult_
            source: sample
```

The yaml above would imply that a module named sample includes the actions `sum_` and `mult_`.
These actions can be defined using the `@arbutus.Arbutus.new_action` wrapper. For example:

```python
import arbutus

@arbutus.Arbutus.new_action
def sum_(*args, **kwargs):
    total = 0
    for number in kwargs['values']:
        total += number
    print(total)
```

Finally, the CLI itself can be constructed by calling the `from_yaml` method:

```python
import arbutus

if __name__ == '__main__':
    cli = arbutus.Arbutus()
    cli.from_yaml('sample/cli.yaml')
    cli.parse_args()
```

The CLI can then be called like:

```bash
# This would display general help about the CLI functionality
python3 sample/sample.py -h
# This would display general help about the sum test functionality
python3 sample/sample.py sum -h
# This would throw the result of running the sum function with the passed arguments
python3 sample/sample.py sum 12 25 3
```


## Roadmap

See the [open issues](https://github.com/aubravo/arbutus/issues) for a full list of proposed features (and known issues).

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Alvaro U. Bravo - [alvaroubravo@gmail.com](mailto:alvaroubravo@gmail.com)

Project Links:
* [arbutus - GitHub](https://github.com/aubravo/arbutus)
* [arbutus - PyPi](https://pypi.org/project/arbutus/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/aubravo/arbutus.svg?style=for-the-badge
[contributors-url]: https://github.com/aubravo/arbutus/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/aubravo/arbutus.svg?style=for-the-badge
[forks-url]: https://github.com/aubravo/arbutus/network/members
[stars-shield]: https://img.shields.io/github/stars/aubravo/arbutus.svg?style=for-the-badge
[stars-url]: https://github.com/aubravo/arbutus/stargazers
[issues-shield]: https://img.shields.io/github/issues/aubravo/arbutus.svg?style=for-the-badge
[issues-url]: https://github.com/aubravo/arbutus/issues
[license-shield]: https://img.shields.io/github/license/aubravo/arbutus.svg?style=for-the-badge
[license-url]: https://github.com/aubravo/arbutus/blob/master/LICENSE
[Python.org]: https://img.shields.io/badge/Python->=3.8-4B8BBE?style=for-the-badge&logo=Python&logoColor=FFD43B
[Python-url]: https://python.org
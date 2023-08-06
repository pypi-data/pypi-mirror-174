# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['line_profiler_extended']

package_data = \
{'': ['*']}

install_requires = \
['line-profiler>=3.5,<4.0', 'pytest>=5,<8']

extras_require = \
{'ipython': ['IPython>=0.13']}

entry_points = \
{'pytest11': ['line_profiler_extended = line_profiler_extended.pytest_plugin']}

setup_kwargs = {
    'name': 'line-profiler-extended',
    'version': '0.0.2',
    'description': "Inherits awesome rkern's line-profiler and adds some useful features",
    'long_description': '# line-profiler-extended\n\n[![PyPI](https://img.shields.io/pypi/v/line-profiler-extended?style=flat-square)](https://pypi.python.org/pypi/line-profiler-extended/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/line-profiler-extended?style=flat-square)](https://pypi.python.org/pypi/line-profiler-extended/)\n[![PyPI - License](https://img.shields.io/pypi/l/line-profiler-extended?style=flat-square)](https://pypi.python.org/pypi/line-profiler-extended/)\n[![Coookiecutter - Wolt](https://img.shields.io/badge/cookiecutter-Wolt-00c2e8?style=flat-square&logo=cookiecutter&logoColor=D4AA00&link=https://github.com/woltapp/wolt-python-package-cookiecutter)](https://github.com/woltapp/wolt-python-package-cookiecutter)\n\n\n---\n\n**Documentation**: [https://utapyngo.github.io/line-profiler-extended](https://utapyngo.github.io/line-profiler-extended)\n\n**Source Code**: [https://github.com/utapyngo/line-profiler-extended](https://github.com/utapyngo/line-profiler-extended)\n\n**PyPI**: [https://pypi.org/project/line-profiler-extended/](https://pypi.org/project/line-profiler-extended/)\n\n---\n\nInherits awesome rkern\'s line-profiler and adds some useful features.\n\n## Installation\n\n```sh\npip install line-profiler-extended\n```\n\n## Using the API\n\n```python\nfrom line_profiler_extended import LineProfilerExtended\n\ndef foo():\n    pass\n\n# profile the foo function\nprofiler = LineProfilerExtended(foo)\n\n# profile all functions from some_module\nimport some_module\nprofiler = LineProfilerExtended(some_module)\n\n# profile all functions from all modules found recursively\n# starting from the grandparent directory of the current file\nfrom pathlib import Path\nprofiler = LineProfilerExtended(Path(__file__).parent.parent)\n\n# profile all functions from all modules found recursively in "path",\n# reporting only functions that took at least 1 millisecond\nprofiler = LineProfilerExtended("path", eps=0.001)\n\n# profile all functions from all modules found recursively in "path" with "m" in module name but without "mm"\nprofiler = LineProfilerExtended("path", include_regex="m", exclude_regex="mm")\n\n# all types of locations can be combined\nprofiler = LineProfilerExtended(\n    Path("/some/path"), "path", some_module, foo,\n    eps=0.001, include_regex="m", exclude_regex="mm"\n)\n\nprofiler.enable_by_count()\nprofiler.runcall(foo)\nprofiler.print_stats()\n```\n\n## Usage with IPython\n\n```ipython\n%load_ext line_profiler_extended\n\n# profile the foo function\n%lpext -p foo foo()\n\n# profile all functions from some_module\n%lpext -p some_module foo()\n\n# profile all functions from all modules found recursively in some path\nfrom pathlib import Path\n%lpext -p Path("/some/path") foo()\n\n# profile all functions from all modules found recursively in "path",\n# reporting only functions that took at least 1 millisecond\n%lpext -p "path" --eps 0.001 foo()\n\n# profile all functions from all modules found recursively in "path" with "m" in module name but without "mm"\n%lpext -p "path" --include "m" --exclude "mm" foo()\n\n# all types of locations can be combined\n%lpext -p Path(__file__).parent.parent -p "path" -p some_module -p foo --eps 0.001 --include "m" --exclude "mm" foo()\n```\n\n## Usage with pytest\n\n```python\nimport pytest\nfrom pathlib import Path\n\n# all args are passed directly to the LineProfilerExtended constructor\n@pytest.mark.line_profile.with_args(Path(__file__).parent.parent, eps=0.01)\ndef test_foo():\n    pass\n```\n\n## Development\n\n* Clone this repository\n* Requirements:\n  * [Poetry](https://python-poetry.org/)\n  * Python 3.7+\n* Create a virtual environment and install the dependencies\n\n```sh\npoetry install\n```\n\n* Activate the virtual environment\n\n```sh\npoetry shell\n```\n\n### Testing\n\n```sh\npytest\n```\n\n### Documentation\n\nThe documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings\n of the public signatures of the source code. The documentation is updated and published as a [Github project page\n ](https://pages.github.com/) automatically as part each release.\n\n### Releasing\n\nTrigger the [Draft release workflow](https://github.com/utapyngo/line-profiler-extended/actions/workflows/draft_release.yml)\n(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.\n\nFind the draft release from the\n[GitHub releases](https://github.com/utapyngo/line-profiler-extended/releases) and publish it. When\n a release is published, it\'ll trigger [release](https://github.com/utapyngo/line-profiler-extended/blob/master/.github/workflows/release.yml) workflow which creates PyPI\n release and deploys updated documentation.\n\n### Pre-commit\n\nPre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality\n checks to make sure the changeset is in good shape before a commit/push happens.\n\nYou can install the hooks with (runs for each commit):\n\n```sh\npre-commit install\n```\n\nOr if you want them to run only for each push:\n\n```sh\npre-commit install -t pre-push\n```\n\nOr if you want e.g. want to run all checks manually for all files:\n\n```sh\npre-commit run --all-files\n```\n\n---\n\nThis project was generated using the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.\n',
    'author': 'Ivan Zaikin',
    'author_email': 'ut@pyngo.tom.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://utapyngo.github.io/line-profiler-extended',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)

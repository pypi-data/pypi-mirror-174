# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pybash']
install_requires = \
['ideas>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'pybash',
    'version': '0.1.1',
    'description': '>execute bash commands from python easily',
    'long_description': '# PyBash\n\nStreamline bash-command execution from python with an easy-to-use syntax. It combines the simplicity of writing bash scripts with the flexibility of python. Behind the scenes, any line starting with `>` is transformed to python `subprocess` calls and then injected into `sys.meta_path` as an import hook. All possible thanks to the wonderful [ideas](https://github.com/aroberge/ideas) project!\n\n\n# Examples\n\n### Simple execution with output\n```python\n>python --version\n>echo \\\\nthis is an echo\n```\noutputs:\n```\nPython 3.9.15\n\nthis is an echo\n```\n\n### Set output to variable and parse\n```python\nout = >cat test.txt\ntest_data = out.decode(\'utf-8\').strip()\nprint(test_data.replace("HELLO", "HOWDY"))\n```\noutputs:\n```\nHOWDY WORLD\n```\n\n### Wrapped, in-line execution and parsing\n```python\nprint((>cat test.txt).decode(\'utf-8\').strip())\n```\noutputs:\n```\nHELLO WORLD\n```\n\n### Redirection\n```python\n>echo "hello" >> test4.txt\n```\n\n### Pipe chaining\n```python\n>cat test.txt | sed \'s/HELLO/HOWDY/g\' | sed \'s/HOW/WHY/g\' | sed \'s/WHY/WHEN/g\'\n```\noutputs:\n```\nWHENDY WORLD\n```\n\n### Redirection chaining\n```python\n>cat test.txt | sed \'s/HELLO/HOWDY\\\\n/g\' > test1.txt >> test2.txt > test3.txt\n```\n\n### Chaining pipes and redirection- works in tandem!\n```python\n>cat test.txt | sed \'s/HELLO/HOWDY\\\\n/g\' > test5.txt\n```\n\n#### Also works inside methods!\n```python\n# PYBASH DEMO #\ndef cp_test():\n    >cp test.txt test_copy.txt\n\ncp_test()\n```\n\n# Usage\n1. `pip install pybash`\n2. `python run.py` OR directly, `python -m ideas demo -a pybash`\n\n\n# TODO\n- Redirection: `>echo "hello" >> test.txt`\n- Pipes: `>cat test.txt | sed \'s/HELLO/HOWDY/g\'`',
    'author': 'Jay',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

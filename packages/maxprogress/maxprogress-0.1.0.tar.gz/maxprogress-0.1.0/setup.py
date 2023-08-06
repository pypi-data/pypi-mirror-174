# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['maxprogress']
install_requires = \
['maxconsole>=0.1.0,<0.2.0', 'rich>=12.6.0,<13.0.0']

entry_points = \
{'console_scripts': ['get_progress = maxprogress:get_progress',
                     'maxprogress = maxprogress:main']}

setup_kwargs = {
    'name': 'maxprogress',
    'version': '0.1.0',
    'description': 'A customized Rich Progress Bar',
    'long_description': '# MaxProgress 0.1.0\n\nMaxprogress provides a thin wrapper around rich’s Progress Bar class. It generates a custom formated progress bar.\n\n<div style="max-width:80%;margin:auto;padding:20px;">\n  <iframe src="maxprogress.gif" width="997" height="164" frameBorder="0" allowFullScreen>maxprogress</iframe>\n</div>div\n\n## Installation\n\n### Pip\n\n```bash\npip install maxprogress\n```\n\n### Pipx\n\n```bash\npipx install maxprogress\n```\n\n### Poetry\n\n```bash\npoetry add maxprogress\n```\n\n## Usage\n\n```python\nfrom maxprogress import get_progress\n\nprogress = get_progress():\n\nwith progress:\n\n    task1 = progress.add_task("[red]Downloading...", total=200)\n    task2 = progress.add_task("[green]Processing...", total=200)\n    task3 = progress.add_task("[cyan]Cooking...", total=200)\n\n    while not progress.finished:\n        progress.update(task1, advance=0.5)\n        progress.update(task2, advance=0.3)\n        progress.update(task3, advance=0.9)\n        time.sleep(0.02)\n\n```',
    'author': 'maxludden',
    'author_email': 'dev@maxludden.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

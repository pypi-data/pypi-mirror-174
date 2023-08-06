# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymyplot']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.0,<4.0.0']

setup_kwargs = {
    'name': 'pymyplot',
    'version': '0.2.2',
    'description': 'Correction of usefull plotting setup for matplotlib',
    'long_description': '# Pymyplot\n\nA collection of useful presets for the visualization of scientific data. It is intended for personal usage but feel free to take a look at it.\n\n> As I noticed, publishing this package to pypi.org appears to be overkill. Nevertheless, I have decided to do so in order to have better access to the library for my own personal use.\n\n## Requirements\n\n- python >= 3.9\n- matplotlib >= 3.6.0\n\n## Installation\n\nYou can use either [poetry](https://python-poetry.org) or pip.\n\n```bash\npip install pymyplot\n# or\npoetry add pymyplot\n```\n\n## Usage\n\n### Basic\n\nIn the module, `myplt` overwrites `matplotlib.pyplot`. This is intended to apply custom `matplotlib.pyplot.rcparams` for a specific plot preset when it is imported. (e.g. `pymyplot.aip`)\n\n```python\n>>> from pymyplot import myplt  # myplt overwrites matplotlib.pyplot\n>>> from pymyplot.basic import Line, Font, Marker\n# Basic presets come with\n# Line: defulat_linewidth = 1.0\n# Font: default_font_size = 12.0, default_family = "sans-serif", default_font = "Helvetica"\n# Marker: default_size = 10.0\n>>> fig, ax = myplt.subplots(...)\n>>> ax.text(..., fontsize=Font.size("small"))\n>>> ax.plot(..., linewidth=Line.width("thin"), marker=Marker.style("solid"))\n>>> ax.scatter(..., s=Marker.size("small"))\n```\n\n### Colors\n\n`pymyplot` uses colors from [TailwindCSS](https://tailwindcss.com). You can access to the colors using TailwindCSS syntax.\n\n```python\n>>> from pymyplot import get_color\n>>> get_color("red-400")\n"#f87171"\n```\n',
    'author': 'Kyoungseoun Chung',
    'author_email': 'kchung@student.ethz.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gdoc',
 'gdoc.app',
 'gdoc.app.compile',
 'gdoc.app.dump',
 'gdoc.app.trace',
 'gdoc.lib',
 'gdoc.lib.gdoc',
 'gdoc.lib.gdoccompiler',
 'gdoc.lib.gdoccompiler.gdcompiler',
 'gdoc.lib.gdocparser',
 'gdoc.lib.gdocparser.tag',
 'gdoc.lib.gdocparser.textblock',
 'gdoc.lib.gobj',
 'gdoc.lib.gobj.types',
 'gdoc.lib.pandocast',
 'gdoc.lib.pandocastobject',
 'gdoc.lib.pandocastobject.pandoc',
 'gdoc.lib.pandocastobject.pandocast',
 'gdoc.lib.pandocastobject.pandocstr',
 'gdoc.lib.types',
 'gdoc.lib.types.table',
 'gdoc.plugin',
 'gdoc.plugin.sysml',
 'gdoc.util']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['gdoc = gdoc.__main__:main']}

setup_kwargs = {
    'name': 'gdoc',
    'version': '0.1.1',
    'description': 'A tool to process GDML(GDoc Markup Language) documents.',
    'long_description': 'None',
    'author': 'Tsuyoshi Kodama',
    'author_email': 'tsuyoshi.kodama@byrnison.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

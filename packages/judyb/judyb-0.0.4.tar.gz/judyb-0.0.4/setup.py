from setuptools import setup

packages = \
['judyb',
 'judyb.exifHeader',
 'judyb.lsb',
 'judyb.lsbset',
 'judyb.red',
 'judyb.steganalysis']

package_data = \
{'': ['*']}

install_requires = \
['crayons>=0.4.0,<0.5.0',
 'opencv-python>=4.5.4,<5.0.0',
 'piexif>=1.1.3,<2.0.0',
 'pillow>=9.0.0,<10.0.0']

entry_points = \
{'console_scripts': ['judyb-lsb = bin.lsb:main',
                     'judyb-lsb-set = bin.lsbset:main',
                     'judyb-red = bin.red:main',
                     'judyb-steganalysis-parity = bin.parity:main',
                     'judyb-steganalysis-statistics = bin.statistics:main']}

setup_kwargs = {
    'name': 'judyb',
    'version': '0.0.4',
    'description': 'A pure Python judyb module.',
    'long_description': '# judyb',
    'author': 'Cédric Bonhomme',
    'author_email': 'cedric@cedricbonhomme.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://sr.ht/~cedric/judyb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)

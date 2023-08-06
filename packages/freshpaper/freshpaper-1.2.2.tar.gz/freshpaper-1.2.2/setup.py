# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['freshpaper']
install_requires = \
['click', 'pillow>=7.0,<8.0']

entry_points = \
{'console_scripts': ['freshpaper = freshpaper:main']}

setup_kwargs = {
    'name': 'freshpaper',
    'version': '1.2.2',
    'description': "Program to automatically set Bing's `Photo of the day` as your Desktop's wallpaper.",
    'long_description': ".. -*-restructuredtext-*-\n\nfreshpaper\n==========\n\n.. image:: https://img.shields.io/pypi/v/freshpaper.svg\n    :target: https://pypi.python.org/pypi/freshpaper\n    :alt: PyPi version\n\n.. image:: https://app.fossa.io/api/projects/git%2Bgithub.com%2Fguptarohit%2Ffreshpaper.svg?type=shield\n    :target: https://app.fossa.io/projects/git%2Bgithub.com%2Fguptarohit%2Ffreshpaper?ref=badge_shield\n    :alt: FOSSA Status\n\n.. image:: https://img.shields.io/pypi/l/freshpaper.svg\n    :target: https://github.com/guptarohit/freshpaper/blob/master/LICENSE\n    :alt: License\n\n.. image:: https://pepy.tech/badge/freshpaper\n    :target: https://pepy.tech/project/freshpaper\n    :alt: Downloads\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n    :alt: Code style: black\n\nfreshpaper automatically sets `Bing <https://www.bing.com/>`_ photo of the day or `NASA-APOD <https://apod.nasa.gov/apod/astropix.html/>`_ or `Random Unsplash photo <https://source.unsplash.com>`_ or `Nat Geo - Photo of the Day <https://www.nationalgeographic.com/photography/photo-of-the-day/>`_ as your desktop's wallpaper. Available for Windows, macOS & Linux.\n\n\nInstallation\n------------\n\n::\n\n    $ pip install freshpaper\n\nUpdate to latest release:\n\n::\n\n    $ pip install -U freshpaper\n\n\nUsage\n------\n\nTo update the wallpaper simply run:\n\n::\n\n    $ freshpaper\n\nThe default source of wallpaper is ``bing``. Available sources: ``bing``, ``nasa``, ``unsplash_random``, ``nat_geo``.\n\nTo change the source of the wallpaper, run:\n\n::\n\n    $ freshpaper --source <source_name>\n    \nHelp command of cli utility:\n\n::\n\n    $ freshpaper --help\n    Usage: freshpaper [OPTIONS] COMMAND [ARGS]...\n\n    Options:\n      --source [bing|nasa|unsplash_random|nat_geo]  Source for setting the wallpaper.\n      --help           Show this message and exit.\n\nContributing\n------------\n\nFeel free to make a pull request! :octocat:\n\nIf you found this useful, I'd appreciate your consideration in the below. ✨🍰\n\n.. image:: https://user-images.githubusercontent.com/7895001/52529389-e2da5280-2d16-11e9-924c-4fe3f309c780.png\n    :target: https://www.buymeacoffee.com/rohitgupta\n    :alt: Buy Me A Coffee\n\n.. image:: https://user-images.githubusercontent.com/7895001/52529390-e8379d00-2d16-11e9-913b-4d09db90403f.png\n    :target: https://www.patreon.com/bePatron?u=14009502\n    :alt: Become a Patron!\n\n\nLicense\n-------\n\n.. image:: https://app.fossa.io/api/projects/git%2Bgithub.com%2Fguptarohit%2Ffreshpaper.svg?type=large\n    :target: https://app.fossa.io/projects/git%2Bgithub.com%2Fguptarohit%2Ffreshpaper?ref=badge_large\n    :alt: FOSSA Status\n",
    'author': 'Rohit Gupta',
    'author_email': 'rohitgtech+git@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/guptarohit/freshpaper',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

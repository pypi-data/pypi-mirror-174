# -*- coding: utf-8 -*-
"""setup.py: setuptools control."""
from setuptools import setup, find_packages
from distutils.util import convert_path

main_ns = {}
with open(convert_path('neolabci/version.py')) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name = 'neolab-ci',
    packages = ['neolabci', 'neolabci.commands'],
    install_requires=['pycurl', 'pyyaml', 'cleo'],
    entry_points = {
        'console_scripts': ['neolab-ci=neolabci.index:main']
    },
    package_data={'neolabci': ['templates/*']},
    version = main_ns['__version__'],
    description = 'Command Line Tool for Neolab  CI service written in Python',
    author = '@Neolab Vietnam',
    author_email = 'phuong.nv@neo-lab.vn',
    url = '',
    classifiers=[
        # Indicate who your project is intended for
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
    ],
    # What does your project relate to?
    keywords='setuptools development neolab-ci',
)
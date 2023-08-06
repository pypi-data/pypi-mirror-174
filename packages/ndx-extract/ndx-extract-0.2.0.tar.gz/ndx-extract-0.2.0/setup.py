# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages
from shutil import copy2

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "requirements.txt")) as f:
    install_requires = f.read().strip().split("\n")

with open("README.md", "r") as f:
    long_description = f.read()

setup_args = {
    'name': 'ndx-extract',
    'version': '0.2.0',
    'description': 'NWB extension for storage of parameters and output of EXTRACT pipeline.',
    'long_description': long_description,
    'long_description_content_type': "text/markdown",
    'author': 'Ben Dichter, Szonja Weigl and Cesar Echavarria',
    'author_email': 'ben.dichter@catalystneuro.com',
    'url': "https://github.com/catalystneuro/ndx-extract",
    'license': 'BSD 3-Clause',
    'install_requires': install_requires,
    'packages': find_packages(where='src/pynwb', exclude=["tests", "tests.*"]),
    'package_dir': {'': 'src/pynwb'},
    'package_data': {'ndx_extract': [
        'spec/ndx-extract.namespace.yaml',
        'spec/ndx-extract.extensions.yaml',
    ]},
    'classifiers': [
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
    'zip_safe': False
}


def _copy_spec_files(project_dir):
    ns_path = os.path.join(project_dir, 'spec', 'ndx-extract.namespace.yaml')
    ext_path = os.path.join(project_dir, 'spec', 'ndx-extract.extensions.yaml')

    dst_dir = os.path.join(project_dir, 'src', 'pynwb', 'ndx_extract', 'spec')
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    copy2(ns_path, dst_dir)
    copy2(ext_path, dst_dir)


if __name__ == '__main__':
    _copy_spec_files(os.path.dirname(__file__))
    setup(**setup_args)

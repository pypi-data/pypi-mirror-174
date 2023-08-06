#!/usr/bin/env python3
# template: https://gitlab.com/jlecomte/projects/python/reference-files

from setuptools import setup
from torxtools.misctools import get_package_about, get_package_requirements

about = get_package_about()
requirements = get_package_requirements()

setup(
    name=about["__title__"],
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__email__"],
    url=about["__uri__"],
    description=about["__summary__"],
    license=about["__license__"],
    install_requires=requirements,
)

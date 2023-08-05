#!/usr/bin/env python3
# template: https://gitlab.com/jlecomte/projects/python/reference-files

from setuptools import setup

with open("requirements.txt", encoding="UTF-8") as fd:
    requirements = fd.read().splitlines()
    requirements = [x for x in requirements if x and not x.startswith("--")]

about = {}
with open("torxtools/__about__.py", encoding="UTF-8") as fd:
    exec(fd.read(), None, about)  # pylint: disable=exec-used
about = {k: v for k, v in about.items() if k.startswith("__")}

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

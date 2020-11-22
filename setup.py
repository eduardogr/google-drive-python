import os
import pathlib

import pkg_resources
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with pathlib.Path('requirements/prod.txt').open() as requirements_txt:
    requirements = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

with pathlib.Path('requirements/dev.txt').open() as requirements_txt:
    extra_requirements_dev = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name="google-drive",
    version="0.1.0",
    author="Eduardo Garcia",
    author_email="garciaruiz.edu+google-drive-python@gmail.com",
    maintainer="Eduardo García",
    maintainer_email="garciaruiz.edu+google-drive-python@gmail.com",
    description=("Manage and interact with your Google Drive"),
    license="Apache",
    keywords="google drive",
    url="https://github.com/eduardogr/google-drive-python",
    packages=['googledrive'],
    install_requires=requirements,
    extras_require={
        'dev': extra_requirements_dev
    },
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: Apache Software License",
    ],
)

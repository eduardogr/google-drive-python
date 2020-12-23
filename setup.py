import os
import pathlib

import pkg_resources
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def read_requirements(path):
    with pathlib.Path(path).open() as requirements_txt:
        return [
            str(requirement)
            for requirement
            in pkg_resources.parse_requirements(requirements_txt)
        ]


requirements = read_requirements('requirements/prod.txt')
extra_requirements_dev = read_requirements('requirements/dev.txt')


setup(
    name="google-drive",
    version="0.3.0",
    author="Eduardo Garcia",
    author_email="garciaruiz.edu+google-drive-python@gmail.com",
    maintainer="Eduardo García",
    maintainer_email="garciaruiz.edu+google-drive-python@gmail.com",
    description=("Library and cli to manage and interact with your Google Drive"),
    license="Apache",
    keywords="google drive",
    url="https://github.com/eduardogr/google-drive-python",
    packages=['googledrive'],
    install_requires=requirements,
    extras_require={
        'dev': extra_requirements_dev
    },
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: Apache Software License",
    ],
    entry_points={
        'console_scripts': ['google-drive = googledrive.cli:googledrive'],
    },
)

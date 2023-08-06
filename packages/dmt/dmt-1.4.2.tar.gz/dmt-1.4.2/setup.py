#!/usr/bin/env python
import os
from setuptools import setup, find_packages
import domain

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()


setup(
    name='dmt',
    author='Danny Waser',
    version=domain.__version__,
    license='LICENSE',
    url='https://gitlab.com/waser-technologies/technologies/dmt',
    project_urls={
        "Documentation": "https://gitlab.com/waser-technologies/technologies/dmt/blob/main/README.md",
        "Code": "https://gitlab.com/waser-technologies/technologies/dmt",
        "Issue tracker": "https://gitlab.com/waser-technologies/technologies/dmt/issues",
    },
    description='Manage domains like packages.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages('.'),
    python_requires='>=3.8,<=3.10.9',
    install_requires = [
        'prompt_toolkit>=2.0.0,<3.1.0',
        'tqdm',
        'halo',
        'pyyaml',
        'requests',
        'transformers',
    ],
    entry_points={
        'console_scripts': [
            'dmt = domain.entry_points.run_dmt:run',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Natural Language :: French",
        # add more languages as they become availible
    ],
)

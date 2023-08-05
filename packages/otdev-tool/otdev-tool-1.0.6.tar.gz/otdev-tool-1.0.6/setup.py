#-*-coding:utf-8-*-
#!/usr/bin/env python

import re
import setuptools
from OntimDevTool import version

with open("README.md", "r") as fh:
  long_description = fh.read()

install_requires = []

setuptools.setup(
    name="otdev-tool",
    version=version,
    packages=setuptools.find_packages(exclude=("test")),
    author="caiyongqing",
    author_email="yongqing.cai@chino-e.com",
    description="Dev tools of Ontim.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://example.com",
    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ),
    entry_points={
        'console_scripts': [
            'otdev-tool = OntimDevTool.main:main'
        ]},
      install_requires=[
        'certifi==2022.9.24',
        'charset-normalizer==2.1.1',
        'idna==3.4',
        'pyfiglet==0.8.post1',
        'requests==2.28.1',
        'urllib3==1.26.12',
      ],
)
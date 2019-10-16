# yafg: Yet Another Figure Generator
#
# Copyright (c) 2019 Philipp Trommler
#
# SPDX-License-Identifier: GPL-3.0-or-later
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()

setuptools.setup(
        author = "Philipp Trommler",
        author_email = "yafg@philipp-trommler.me",
        classifiers = [
            "Development Status :: 4 - Beta",
            "Environment :: Plugins",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: Implementation :: CPython",
            "Topic :: Documentation",
            "Topic :: Text Processing :: Markup",
        ],
        description = "Figure and figcaption generator markdown extension",
        entry_points = {
            "markdown.extensions": ["yafg = yafg:YafgExtension"]
        },
        install_requires = requirements,
        keywords = "markdown image figure caption html a11y",
        license = "GPLv3+",
        long_description = long_description,
        long_description_content_type = "text/markdown",
        maintainer = "Philipp Trommler",
        maintainer_email = "yafg@philipp-trommler.me",
        name = "yafg",
        packages = setuptools.find_packages(),
        python_requires = ">=2.7.15, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, <4",
        url = "https://git.sr.ht/~ferruck/yafg",
        version = "0.2",
)

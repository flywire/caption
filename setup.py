# yafg: Yet Another Figure Generator
#
# Copyright (c) 2019 Philipp Trommler
#
# SPDX-License-Identifier: GPL-3.0-or-later
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

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
            "Topic :: Documentation",
            "Topic :: Text Processing :: Markup",
        ],
        description = "Figure and figcaption generator markdown extension",
        entry_points = {
            "markdown.extensions": ["yafg = yafg:YafgExtension"]
        },
        install_requires = [
            "Markdown>=3.1.1",
            "setuptools>=36",
        ],
        keywords = "markdown image figure caption html a11y",
        license = "GPLv3+",
        long_description = long_description,
        long_description_content_type = "text/markdown",
        maintainer = "Philipp Trommler",
        maintainer_email = "yafg@philipp-trommler.me",
        name = "yafg",
        packages = setuptools.find_packages(),
        python_requires = ">=2.7.15",
        url = "https://git.sr.ht/~ferruck/yafg",
        version = "0.1",
)

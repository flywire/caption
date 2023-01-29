# caption - Manage markdown captions
#
# Copyright (c) 2020-2023 flywire
# Copyright (c) 2023 sanzoghenzo
# forked from yafg - https://git.sr.ht/~ferruck/yafg
# Copyright (c) 2019 Philipp Trommler
#
# SPDX-License-Identifier: GPL-3.0-or-later
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()

setuptools.setup(
    author="flywire",
    author_email="flywire0@gmail.com",
    classifiers=[
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
    description="Manage markdown captions extension",
    entry_points={
        "markdown.extensions": [
            "caption = caption:CaptionExtension",
            "image_captions = caption:ImageCaptionExtension",
            "table_captions = caption:TableCaptionExtension",
        ]
    },
    install_requires=requirements,
    keywords="markdown image figure caption html a11y",
    license="GPLv3+",
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer="flywire",
    maintainer_email="flywire0@gmail.com",
    name="caption",
    packages=setuptools.find_packages(),
    python_requires=">=2.7.15, >=3, <4",
    url="https://github.com/flywire/caption",
    version="0.2.3",
)

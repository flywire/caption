# caption - Manage markdown captions
#
# Copyright (c) 2020-2023 flywire
# Copyright (c) 2023 sanzoghenzo
# forked from yafg - https://git.sr.ht/~ferruck/yafg
# Copyright (c) 2019 Philipp Trommler
#
# SPDX-License-Identifier: GPL-3.0-or-later
import markdown

from caption.caption import CaptionExtension


def test_listing():
    in_string = """\
Listing: Simple listing test"""
    expected_string = """\
<div class="listing" id="_listing-1">
<figcaption><span>Listing&nbsp;1:</span> Simple listing test</figcaption>
</div>"""
    out_string = markdown.markdown(in_string, extensions=[CaptionExtension()])
    assert out_string == expected_string

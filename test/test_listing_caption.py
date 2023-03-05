# caption - Manage markdown captions
#
# Copyright (c) 2020-2023 flywire
# Copyright (c) 2023 sanzoghenzo
# Copyright (c) 2023 Hendrik Polczynski
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


def test_listing_attr_list():
    in_string = """\
Listing: Simple listing test\n\
{#testid .testclass}"""
    expected_string = """\
<div class="listing testclass" id="testid">
<figcaption><span>Listing&nbsp;1:</span> Simple listing test</figcaption>
</div>"""
    out_string = markdown.markdown(in_string, extensions=["attr_list", CaptionExtension()])
    assert out_string == expected_string


def test_listing_preserve_numbering():
    in_string = """\
Listing 123: Simple listing test"""
    expected_string = """\
<div class="listing" id="_listing-123">
<figcaption><span>Listing&nbsp;123:</span> Simple listing test</figcaption>
</div>"""
    out_string = markdown.markdown(
        in_string,
        extensions=[
            CaptionExtension(
                numbering_preserve=True,
            )
        ],
    )
    assert out_string == expected_string


def test_listing_custom_match_re():
    in_string = """\
Abbildung 123: Simple listing test"""
    expected_string = """\
<div class="listing" id="_listing-1">
<figcaption><span>Listing&nbsp;1:</span> Simple listing test</figcaption>
</div>"""
    out_string = markdown.markdown(
        in_string,
        extensions=[
            CaptionExtension(
                caption_match_re=r"^(?:Listing|Abbildung)\s*?(?P<number>\d*)\:\s*(?P<title>.*)",
            )
        ],
    )
    assert out_string == expected_string


def test_listing_skip_without_title():
    in_string = """\
Listing 123:"""
    expected_string = """\
<p>Listing 123:</p>"""
    out_string = markdown.markdown(
        in_string,
        extensions=[
            CaptionExtension(
                caption_skip_empty=True,
            )
        ],
    )
    assert out_string == expected_string


def test_listing_dont_skip_filled_title():
    in_string = """\
Listing: Simple listing test"""
    expected_string = """\
<div class="listing" id="_listing-1">
<figcaption><span>Listing&nbsp;1:</span> Simple listing test</figcaption>
</div>"""
    out_string = markdown.markdown(
        in_string,
        extensions=[
            CaptionExtension(
                caption_skip_empty=True,
            )
        ],
    )
    assert out_string == expected_string


def test_listing_attr_list_skip_without_title():
    in_string = """\
Listing: \n\
{#testid .testclass}"""
    expected_string = """\
<p class="testclass" id="testid">Listing: </p>"""
    out_string = markdown.markdown(
        in_string,
        extensions=[
            "attr_list",
            CaptionExtension(
                caption_skip_empty=True,
            )
        ],
    )
    assert out_string == expected_string

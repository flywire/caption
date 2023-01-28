# caption - Manage markdown captions
#
# Copyright (c) 2020-2023 flywire
# Copyright (c) 2023 sanzoghenzo
# forked from yafg - https://git.sr.ht/~ferruck/yafg
# Copyright (c) 2019 Philipp Trommler
#
# SPDX-License-Identifier: GPL-3.0-or-later
import markdown

from caption import CaptionExtension
from caption import ImageCaptionExtension


def test_empty_input():
    in_string = ""
    out_string = markdown.markdown(in_string, extensions=[ImageCaptionExtension()])
    assert out_string == in_string


def test_no_images():
    in_string = """\
This is a test text.

It contains multiple paragraphs as well as [links](https://example.com).

* Itemize
* is
* used,
* as well.

# This is a headline.

Nothing should change here whilst using caption."""
    expected_string = markdown.markdown(in_string)
    out_string = markdown.markdown(in_string, extensions=[ImageCaptionExtension()])
    assert out_string == expected_string


def test_listing():
    in_string = """\
Listing: Simple listing test"""
    expected_string = """\
<div class=listing id="_listing-1">
<figcaption><span>Listing&nbsp;1:</span> Simple listing test</figcaption>
</div class=listing>"""
    out_string = markdown.markdown(in_string, extensions=[CaptionExtension()])
    assert out_string == expected_string


def test_simple_image():
    in_string = """\
![alt text](/path/to/image.png "Title")"""
    expected_string = """\
<figure id="_figure-1">
<img alt="alt text" src="/path/to/image.png" />
<figcaption><span>Figure&nbsp;1:</span> Title</figcaption>
</figure>"""
    out_string = markdown.markdown(in_string, extensions=[ImageCaptionExtension()])
    assert out_string == expected_string


def test_simple_image_without_title():
    in_string = """\
![alt text](/path/to/image.png)"""
    expected_string = """\
<figure id="_figure-1">
<img alt="alt text" src="/path/to/image.png" />
<figcaption><span>Figure&nbsp;1</span></figcaption>
</figure>"""
    out_string = markdown.markdown(in_string, extensions=[ImageCaptionExtension()])
    assert out_string == expected_string


def test_multiline_alt():
    in_string = """\
![This is a rather long alt text that spans multiple lines. This may be
necessary to describe a picture for the blind.](/path/to/image.png "Title")"""
    expected_string = """\
<figure id="_figure-1">
<img alt="This is a rather long alt text that spans multiple lines. This may be
necessary to describe a picture for the blind." src="/path/to/image.png" />
<figcaption><span>Figure&nbsp;1:</span> Title</figcaption>
</figure>"""
    out_string = markdown.markdown(in_string, extensions=[ImageCaptionExtension()])
    assert out_string == expected_string


def test_multiline_title():
    in_string = """\
![alt text](/path/to/image.png "This is a very long title. It is used to give
the readers a good figcaption. It may contain a description of the image as well
as sources.")"""
    expected_string = """\
<figure id="_figure-1">
<img alt="alt text" src="/path/to/image.png" />
<figcaption><span>Figure&nbsp;1:</span> This is a very long title. It is used to give the readers a good figcaption. It may contain a description of the image as well as sources.</figcaption>
</figure>"""
    out_string = markdown.markdown(in_string, extensions=[ImageCaptionExtension()])
    assert out_string == expected_string


def test_multiline_title_no_strip():
    in_string = """\
![alt text](/path/to/image.png "This is a very long title. It is used to give the readers a good figcaption. It may contain a description of the image as well as sources.")"""
    expected_string = """\
<figure id="_figure-1">
<img alt="alt text" src="/path/to/image.png" title="This is a very long title. It is used to give the readers a good figcaption. It may contain a description of the image as well as sources." />
<figcaption>This is a very long title. It is used to give the readers a good figcaption. It may contain a description of the image as well as sources.</figcaption>
</figure>"""
    out_string = markdown.markdown(
        in_string,
        extensions=[
            ImageCaptionExtension(
                strip_title=False,
                caption_prefix="",
                numbering=False,
            )
        ],
    )
    assert out_string == expected_string


def test_strip_title_none():
    in_string = """\
![alt text](/path/to/image.png "Title")"""
    expected_string = """\
<figure id="_figure-1">
<img alt="alt text" src="/path/to/image.png" title="Title" />
<figcaption><span>Figure&nbsp;1:</span> Title</figcaption>
</figure>"""
    out_string = markdown.markdown(
        in_string, extensions=[ImageCaptionExtension(strip_title=False)]
    )
    assert out_string == expected_string


def test_content_class():
    in_string = """\
![alt text](/path/to/image.png "Title")"""
    expected_string = """\
<figure class="testclass" id="_figure-1">
<img alt="alt text" src="/path/to/image.png" />
<figcaption><span>Figure&nbsp;1:</span> Title</figcaption>
</figure>"""
    out_string = markdown.markdown(
        in_string, extensions=[ImageCaptionExtension(content_class="testclass")]
    )
    assert out_string == expected_string


def test_caption_class():
    in_string = """\
![alt text](/path/to/image.png "Title")"""
    expected_string = """\
<figure id="_figure-1">
<img alt="alt text" src="/path/to/image.png" />
<figcaption class="testclass"><span>Figure&nbsp;1:</span> Title</figcaption>
</figure>"""
    out_string = markdown.markdown(
        in_string, extensions=[ImageCaptionExtension(caption_class="testclass")]
    )
    assert out_string == expected_string


def test_numbering_false():
    in_string = """\
![alt text](/path/to/image.png "Title")

![alt text 2](/path/to/image2.png "Title 2")"""
    expected_string = """\
<figure id="_figure-1">
<img alt="alt text" src="/path/to/image.png" />
<figcaption>Title</figcaption>
</figure>
<figure id="_figure-2">
<img alt="alt text 2" src="/path/to/image2.png" />
<figcaption>Title 2</figcaption>
</figure>"""
    out_string = markdown.markdown(
        in_string, extensions=[ImageCaptionExtension(numbering=False)]
    )
    assert out_string == expected_string


def test_caption_prefix_class():
    in_string = """\
![alt text](/path/to/image.png "Title")"""
    expected_string = """\
<figure id="_figure-1">
<img alt="alt text" src="/path/to/image.png" />
<figcaption><span class="testclass">Figure&nbsp;1:</span> Title</figcaption>
</figure>"""
    out_string = markdown.markdown(
        in_string,
        extensions=[ImageCaptionExtension(caption_prefix_class="testclass")],
    )
    assert out_string == expected_string


def test_caption_prefix():
    in_string = """\
![alt text](/path/to/image.png "Title")"""
    expected_string = """\
<figure id="_figure-1">
<img alt="alt text" src="/path/to/image.png" />
<figcaption><span>Abbildung&nbsp;1:</span> Title</figcaption>
</figure>"""
    out_string = markdown.markdown(
        in_string, extensions=[ImageCaptionExtension(caption_prefix="Abbildung")]
    )
    assert out_string == expected_string


def test_attribute_preservation():
    in_string = """\
![alt text](/path/to/image.png "Title"){: #someid .someclass somekey='some value' }"""
    expected_string = """\
<figure id="_figure-1">
<img alt="alt text" class="someclass" id="someid" somekey="some value" src="/path/to/image.png" />
<figcaption><span>Figure&nbsp;1:</span> Title</figcaption>
</figure>"""
    out_string = markdown.markdown(
        in_string, extensions=["attr_list", ImageCaptionExtension()]
    )
    assert out_string == expected_string


def test_image_in_link():
    in_string = """\
[![alt text](/path/to/image.png "Title")](/path/to/link.html)"""
    expected_string = """\
<figure id="_figure-1">
<a href="/path/to/link.html"><img alt="alt text" src="/path/to/image.png" /></a>
<figcaption><span>Figure&nbsp;1:</span> Title</figcaption>
</figure>"""
    out_string = markdown.markdown(in_string, extensions=[ImageCaptionExtension()])
    assert out_string == expected_string


def test_combined_options():
    in_string = """\
![alt text](/path/to/image.png "Title")"""
    expected_string = """\
<figure class="testclass1" id="_figure-1">
<img alt="alt text" src="/path/to/image.png" />
<figcaption class="testclass2"><span class="testclass3">Abbildung&nbsp;1:</span> Title</figcaption>
</figure>"""
    out_string = markdown.markdown(
        in_string,
        extensions=[
            ImageCaptionExtension(
                caption_prefix="Abbildung",
                numbering=True,
                content_class="testclass1",
                caption_class="testclass2",
                caption_prefix_class="testclass3",
                strip_title=True,
            )
        ],
    )
    assert out_string == expected_string

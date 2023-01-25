# caption - Manage markdown captions
#
# Copyright (c) 2020 flywire
# forked from yafg - https://git.sr.ht/~ferruck/yafg
# Copyright (c) 2019 Philipp Trommler
#
# SPDX-License-Identifier: GPL-3.0-or-later
import markdown
import unittest

import caption

class captionTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty_input(self):
        inString = ""
        outString = markdown.markdown(inString, extensions = [caption.captionExtension()])
        self.assertEqual(inString, outString)

    def test_no_images(self):
        inString = """\
This is a test text.

It contains multiple paragraphs as well as [links](https://example.com).

* Itemize
* is
* used,
* as well.

# This is a headline.

Nothing should change here whilst using caption."""
        expectedString = markdown.markdown(inString)
        outString = markdown.markdown(inString, extensions = [caption.captionExtension()])
        self.assertEqual(expectedString, outString)

    def test_listing(self):
        inString = """\
Listing: Simple listing test"""
        expectedString = """\
<div class=listing id="_listing-1">
<figcaption><span>Listing&nbsp;1:</span> Simple listing test</figcaption>
</div class=listing>"""
        outString = markdown.markdown(inString, extensions = [caption.captionExtension()])
        self.assertEqual(expectedString, outString)

    def test_simple_image(self):
        inString = """\
![alt text](/path/to/image.png "Title")"""
        expectedString = """\
<figure id="_figure-1">
<img alt="alt text" src="/path/to/image.png" />
<figcaption><span>Figure&nbsp;1:</span> Title</figcaption>
</figure>"""
        outString = markdown.markdown(inString, extensions = [caption.captionExtension()])
        self.assertEqual(expectedString, outString)

    def test_simple_image_without_title(self):
        inString = """\
![alt text](/path/to/image.png)"""
        expectedString = """\
<figure id="_figure-1">
<img alt="alt text" src="/path/to/image.png" />
<figcaption><span>Figure&nbsp;1</span></figcaption>
</figure>"""
        outString = markdown.markdown(inString, extensions = [caption.captionExtension()])
        self.assertEqual(expectedString, outString)

    def test_multiline_alt(self):
        inString = """\
![This is a rather long alt text that spans multiple lines. This may be
necessary to describe a picture for the blind.](/path/to/image.png "Title")"""
        expectedString = """\
<figure id="_figure-1">
<img alt="This is a rather long alt text that spans multiple lines. This may be
necessary to describe a picture for the blind." src="/path/to/image.png" />
<figcaption><span>Figure&nbsp;1:</span> Title</figcaption>
</figure>"""
        outString = markdown.markdown(inString, extensions = [caption.captionExtension()])
        self.assertEqual(expectedString, outString)

    def test_multiline_title(self):
        inString = """\
![alt text](/path/to/image.png "This is a very long title. It is used to give
the readers a good figcaption. It may contain a description of the image as well
as sources.")"""
        expectedString = """\
<figure>
<img alt="alt text" src="/path/to/image.png" title="This is a very long title. It is used to give
the readers a good figcaption. It may contain a description of the image as well
as sources." />
<figcaption>This is a very long title. It is used to give
the readers a good figcaption. It may contain a description of the image as well
as sources.</figcaption>
</figure>"""

    def test_strip_title_none(self):
        inString = """\
![alt text](/path/to/image.png "Title")"""
        expectedString = """\
<figure id="_figure-1">
<img alt="alt text" src="/path/to/image.png" title="Title" />
<figcaption><span>Figure&nbsp;1:</span> Title</figcaption>
</figure>"""
        outString = markdown.markdown(inString, extensions = [caption.captionExtension(link_process="none")])
        self.assertEqual(expectedString, outString)

    def test_content_class(self):
        inString = """\
![alt text](/path/to/image.png "Title")"""
        expectedString = """\
<figure class="testclass" id="_figure-1">
<img alt="alt text" src="/path/to/image.png" />
<figcaption><span>Figure&nbsp;1:</span> Title</figcaption>
</figure>"""
        outString = markdown.markdown(inString, extensions = [caption.captionExtension(content_class="testclass")])
        self.assertEqual(expectedString, outString)

    def test_caption_class(self):
        inString = """\
![alt text](/path/to/image.png "Title")"""
        expectedString = """\
<figure id="_figure-1">
<img alt="alt text" src="/path/to/image.png" />
<figcaption class="testclass"><span>Figure&nbsp;1:</span> Title</figcaption>
</figure>"""
        outString = markdown.markdown(inString, extensions = [caption.captionExtension(caption_class="testclass")])
        self.assertEqual(expectedString, outString)

    def test_numbering_false(self):
        inString = """\
![alt text](/path/to/image.png "Title")

![alt text 2](/path/to/image2.png "Title 2")"""
        expectedString = """\
<figure id="_figure-1">
<img alt="alt text" src="/path/to/image.png" />
<figcaption>Title</figcaption>
</figure>
<figure id="_figure-2">
<img alt="alt text 2" src="/path/to/image2.png" />
<figcaption>Title 2</figcaption>
</figure>"""
        outString = markdown.markdown(inString, extensions = [caption.captionExtension(numbering=False)])
        self.assertEqual(expectedString, outString)

    def test_caption_prefix_class(self):
        inString = """\
![alt text](/path/to/image.png "Title")"""
        expectedString = """\
<figure id="_figure-1">
<img alt="alt text" src="/path/to/image.png" />
<figcaption><span class="testclass">Figure&nbsp;1:</span> Title</figcaption>
</figure>"""
        outString = markdown.markdown(inString, extensions = [caption.captionExtension(caption_prefix_class="testclass")])
        self.assertEqual(expectedString, outString)

    def test_caption_prefix(self):
        inString = """\
![alt text](/path/to/image.png "Title")"""
        expectedString = """\
<figure id="_figure-1">
<img alt="alt text" src="/path/to/image.png" />
<figcaption><span>Abbildung&nbsp;1:</span> Title</figcaption>
</figure>"""
        outString = markdown.markdown(inString, extensions = [caption.captionExtension(caption_prefix="Abbildung")])
        self.assertEqual(expectedString, outString)


    def test_attribute_preservation(self):
        inString = """\
![alt text](/path/to/image.png "Title"){: #someid .someclass somekey='some value' }"""
        expectedString = """\
<figure id="_figure-1">
<img alt="alt text" class="someclass" id="someid" somekey="some value" src="/path/to/image.png" />
<figcaption><span>Figure&nbsp;1:</span> Title</figcaption>
</figure>"""
        outString = markdown.markdown(inString, extensions = ["attr_list", caption.captionExtension()])
        self.assertEqual(expectedString, outString)

    def test_image_in_link(self):
        inString = """\
[![alt text](/path/to/image.png "Title")](/path/to/link.html)"""
        expectedString = """\
<figure id="_figure-1">
<a href="/path/to/link.html"><img alt="alt text" src="/path/to/image.png" /></a>
<figcaption><span>Figure&nbsp;1:</span> Title</figcaption>
</figure>"""
        outString = markdown.markdown(inString, extensions = [caption.captionExtension()])
        self.assertEqual(expectedString, outString)


    def test_combined_options(self):
        inString = """\
![alt text](/path/to/image.png "Title")"""
        expectedString = """\
<figure class="testclass1" id="_figure-1">
<img alt="alt text" src="/path/to/image.png" />
<figcaption class="testclass2"><span class="testclass3">Abbildung&nbsp;1:</span> Title</figcaption>
</figure>"""
        outString = markdown.markdown(inString, extensions = [caption.captionExtension(caption_prefix="Abbildung", numbering=True, content_class="testclass1", caption_class="testclass2", caption_prefix_class="testclass3", link_process="strip_title")])
        self.assertEqual(expectedString, outString)

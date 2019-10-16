# yafg: Yet Another Figure Generator
#
# Copyright (c) 2019 Philipp Trommler
#
# SPDX-License-Identifier: GPL-3.0-or-later
import markdown
import unittest

import yafg

class YafgTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty_input(self):
        inString = ""
        outString = markdown.markdown(inString, extensions = [yafg.YafgExtension()])
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

Nothing should change here whilst using yafg."""
        expectedString = markdown.markdown(inString)
        outString = markdown.markdown(inString, extensions = [yafg.YafgExtension()])
        self.assertEqual(expectedString, outString)

    def test_simple_image(self):
        inString = """\
![alt text](/path/to/image.png "Title")"""
        expectedString = """\
<figure>
<img alt="alt text" src="/path/to/image.png" title="Title" />
<figcaption>Title</figcaption>
</figure>"""
        outString = markdown.markdown(inString, extensions = [yafg.YafgExtension()])
        self.assertEqual(expectedString, outString)

    def test_multiline_alt(self):
        inString = """\
![This is a rather long alt text that spans multiple lines. This may be
necessary to describe a picture for the blind.](/path/to/image.png "Title")"""
        expectedString = """\
<figure>
<img alt="This is a rather long alt text that spans multiple lines. This may be
necessary to describe a picture for the blind." src="/path/to/image.png" title="Title" />
<figcaption>Title</figcaption>
</figure>"""
        outString = markdown.markdown(inString, extensions = [yafg.YafgExtension()])
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

    def test_strip_title(self):
        inString = """\
![alt text](/path/to/image.png "Title")"""
        expectedString = """\
<figure>
<img alt="alt text" src="/path/to/image.png" />
<figcaption>Title</figcaption>
</figure>"""
        outString = markdown.markdown(inString, extensions = [yafg.YafgExtension(stripTitle=True)])
        self.assertEqual(expectedString, outString)

    def test_figure_class(self):
        inString = """\
![alt text](/path/to/image.png "Title")"""
        expectedString = """\
<figure class="testclass">
<img alt="alt text" src="/path/to/image.png" title="Title" />
<figcaption>Title</figcaption>
</figure>"""
        outString = markdown.markdown(inString, extensions = [yafg.YafgExtension(figureClass="testclass")])
        self.assertEqual(expectedString, outString)

    def test_figcaption_class(self):
        inString = """\
![alt text](/path/to/image.png "Title")"""
        expectedString = """\
<figure>
<img alt="alt text" src="/path/to/image.png" title="Title" />
<figcaption class="testclass">Title</figcaption>
</figure>"""
        outString = markdown.markdown(inString, extensions = [yafg.YafgExtension(figcaptionClass="testclass")])
        self.assertEqual(expectedString, outString)

    def test_combined_options(self):
        inString = """\
![alt text](/path/to/image.png "Title")"""
        expectedString = """\
<figure class="testclass1">
<img alt="alt text" src="/path/to/image.png" />
<figcaption class="testclass2">Title</figcaption>
</figure>"""
        outString = markdown.markdown(inString, extensions = [yafg.YafgExtension(stripTitle=True, figureClass="testclass1", figcaptionClass="testclass2")])
        self.assertEqual(expectedString, outString)

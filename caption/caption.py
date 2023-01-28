"""
caption - Manage markdown captions

Applying style and auto-numbering to Python-Markdown content.

https://github.com/flywire/caption
Copyright (c) 2020-2023 flywire
Copyright (c) 2023 sanzoghenzo
forked from yafg - https://git.sr.ht/~ferruck/yafg
Copyright (c) 2019-2020 Philipp Trommler

SPDX-License-Identifier: GPL-3.0-or-later
"""

from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from xml.etree import ElementTree


class CaptionTreeprocessor(Treeprocessor):
    """Base class for Caption processors."""

    name = ""
    content_tag = ""
    caption_tag = "figcaption"

    def __init__(
        self,
        md=None,
        caption_prefix="",
        numbering=True,
        caption_prefix_class=None,
        caption_class=None,
        content_class=None,
        link_process=None,
    ):
        self.caption_prefix = caption_prefix
        self.numbering = numbering
        self.number = 0
        self.caption_prefix_class = caption_prefix_class
        self.caption_class = caption_class
        self.content_class = content_class
        self.link_process = link_process

    def build_content_element(self, par):
        """Format the content element containing the caption"""
        attrib = par.attrib
        par.clear()
        par.tag = self.content_tag
        for k, v in attrib.items():
            par.set(k, v)
        if self.content_class:
            par.set("class", self.content_class)
        par.set("id", "_{}-{}".format(self.name, self.number))
        par.text = "\n"
        par.tail = "\n"

    def build_caption_element(self, par, title):
        """Format the caption."""
        caption = ElementTree.SubElement(par, self.caption_tag)
        caption.tail = "\n"

        if self.caption_class:
            caption.set("class", self.caption_class)
        if not self.numbering:
            caption.text = title
            return
        caption_prefix_span = ElementTree.SubElement(caption, "span")
        if title:
            caption_prefix_span.text = "{}&nbsp;{}:".format(
                self.caption_prefix, self.number
            )
            caption_prefix_span.tail = " {}".format(title)
        else:
            caption_prefix_span.text = "{}&nbsp;{}".format(
                self.caption_prefix, self.number
            )
            caption_prefix_span.tail = ""
        if self.caption_prefix_class:
            caption_prefix_span.set("class", self.caption_prefix_class)

    def matches(self, par):
        """
        Whether the element tree part matches the object to be captioned.

        This will be overriden by the subclasses.
        """
        raise NotImplementedError

    def get_title(self, par):
        """Title of the element. This will be overriden by the subclasses."""
        raise NotImplementedError

    def run(self, root):
        """Find and format all captions."""
        for par in root.findall("./p"):
            if not self.matches(par):
                continue
            self.number += 1
            title = self.get_title(par)
            self.build_content_element(par)
            self.build_caption_element(par, title)


class ListingCaptionTreeProcessor(CaptionTreeprocessor):
    name = "listing"
    content_tag = "div class=listing"

    def matches(self, par):
        return par.text and par.text.startswith("Listing: ")

    def get_title(self, par):
        return par.text[9:]


class FigureCaptionTreeProcessor(CaptionTreeprocessor):
    name = "figure"
    content_tag = "figure"

    def matches(self, par):
        self._a = None
        self._img = par.find("./img")
        if self._img is None:
            self._a = par.find("./a")
            if self._a is None:
                return False
            self._img = self._a.find("./img")
        return self._img is not None

    def get_title(self, par):
        return self._img.get("title")

    def build_content_element(self, par):
        super(FigureCaptionTreeProcessor, self).build_content_element(par)
        if self._a is not None:
            self._a.tail = "\n"
            par.append(self._a)
        else:
            self._img.tail = self._img.tail or "" + "\n"
            par.append(self._img)

    def build_caption_element(self, par, title):
        super(FigureCaptionTreeProcessor, self).build_caption_element(par, title)
        if self.link_process == "strip_title" and title:
            del self._img.attrib["title"]


class TableCaptionTreeProcessor(CaptionTreeprocessor):
    name = "table"
    content_tag = "div class=table"
    caption_tag = "caption"
    # link_process = self.link_process or "line_2_caption",

    def matches(self, par):
        return par.text and par.text.startswith("Table: ")

    def get_title(self, par):
        return par.text[7:]


class CaptionExtension(Extension):
    # caption Extension

    def __init__(self, **kwargs):
        # Setup configs
        self.config = {
            "figure_caption_prefix": [
                "Figure",
                "The text to show in front of the image caption.",
            ],
            "table_caption_prefix": [
                "Table",
                "The text to show in front of the table caption.",
            ],
            "listing_caption_prefix": [
                "Listing",
                "The text to show in front of the listing caption.",
            ],
            "numbering": [True, "Add the caption number to the prefix."],
            "caption_prefix_class": [
                "",
                "CSS class to add to the caption prefix <span /> element.",
            ],
            "caption_class": ["", "CSS class to add to the caption element."],
            "content_class": ["", "CSS class to add to the content element."],
            "link_process": ["", "Some content types support linked processes."],
        }
        super(CaptionExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        # Add pieces to Markdown
        numbering = self.getConfig("numbering")
        caption_prefix_class = self.getConfig("caption_prefix_class")
        caption_class = self.getConfig("caption_class")
        content_class = self.getConfig("content_class")
        link_process = self.getConfig("link_process")

        md.treeprocessors.register(
            FigureCaptionTreeProcessor(
                md,
                caption_prefix=self.getConfig("figure_caption_prefix"),
                numbering=numbering,
                caption_prefix_class=caption_prefix_class,
                caption_class=caption_class,
                content_class=content_class,
                link_process=link_process or "strip_title",
            ),
            "figurecaptiontreeprocessor",
            8,
        )
        md.treeprocessors.register(
            TableCaptionTreeProcessor(
                md,
                caption_prefix=self.getConfig("table_caption_prefix"),
                numbering=numbering,
                caption_prefix_class=caption_prefix_class,
                caption_class=caption_class,
                content_class=content_class,
                link_process=link_process,
            ),
            "tablecaptiontreeprocessor",
            8,
        )
        md.treeprocessors.register(
            ListingCaptionTreeProcessor(
                md,
                caption_prefix=self.getConfig("listing_caption_prefix"),
                numbering=numbering,
                caption_prefix_class=caption_prefix_class,
                caption_class=caption_class,
                content_class=content_class,
                link_process=link_process,
            ),
            "listingcaptiontreeprocessor",
            8,
        )


def makeExtension(**kwargs):
    return CaptionExtension(**kwargs)

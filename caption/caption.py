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
        caption_top=True,
    ):
        self.caption_prefix = caption_prefix
        self.numbering = numbering
        self.number = 0
        self.caption_prefix_class = caption_prefix_class
        self.caption_class = caption_class
        self.content_class = content_class
        self.link_process = link_process
        self.caption_top = caption_top

    def build_content_element(self, par, caption, replace=True):
        """Format the content element containing the caption"""
        attrib = par.attrib
        if replace:
            par.clear()
        par.tag = self.content_tag
        for k, v in attrib.items():
            par.set(k, v)

        if self.content_class:
            if not "class" in attrib:
                par.set("class", self.content_class)
            else:
                par.set("class", self.content_class + " " + attrib["class"])

        if not "id" in attrib:
            par.set("id", "_{}-{}".format(self.name, self.number))
            
        if replace:
            par.text = "\n"
        par.tail = "\n"

    def add_caption_to_content(self, content, caption):
        if self.caption_top:
            content.insert(0, caption)
        else:
            content.append(caption)

    def build_caption_element(self, title):
        """Format the caption."""
        caption = ElementTree.Element(self.caption_tag)
        caption.tail = "\n"

        if self.caption_class:
            caption.set("class", self.caption_class)
        if not self.numbering:
            caption.text = title
            return caption
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
        return caption

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
            caption = self.build_caption_element(title)
            self.build_content_element(par, caption)
            self.add_caption_to_content(par, caption)


class ListingCaptionTreeProcessor(CaptionTreeprocessor):
    name = "listing"
    content_tag = "div"

    def matches(self, par):
        return par.text and par.text.startswith("Listing: ")

    def get_title(self, par):
        return par.text[9:]


class CaptionExtension(Extension):
    # caption Extension

    def __init__(self, **kwargs):
        # Setup configs
        self.config = {
            "caption_prefix": [
                "Listing",
                "The text to show in front of the listing caption.",
            ],
            "numbering": [True, "Add the caption number to the prefix."],
            "caption_prefix_class": [
                "",
                "CSS class to add to the caption prefix <span /> element.",
            ],
            "caption_class": ["", "CSS class to add to the caption element."],
            "content_class": ["listing", "CSS class to add to the content element."],
            "link_process": ["", "Some content types support linked processes."],
            "caption_top": [False, "Put the caption at the top of the content."],
        }
        super(CaptionExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.treeprocessors.register(
            ListingCaptionTreeProcessor(md, **self.getConfigs()),
            "listingcaptiontreeprocessor",
            8,
        )


def makeExtension(**kwargs):
    return CaptionExtension(**kwargs)

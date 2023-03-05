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
import re


class CaptionTreeprocessor(Treeprocessor):
    """Base class for Caption processors."""

    name = ""
    content_tag = ""
    caption_tag = "figcaption"

    def __init__(
        self,
        md=None,
        caption_prefix="",
        caption_match_re="",
        caption_skip_empty=False,
        numbering=True,
        numbering_preserve=False,
        caption_prefix_class=None,
        caption_class=None,
        content_class=None,
        link_process=None,
        caption_top=True,
    ):
        self.caption_prefix = caption_prefix
        self.caption_match_re = caption_match_re
        self._match_re = re.compile(self.caption_match_re)
        self.caption_skip_empty = caption_skip_empty,
        self.numbering = numbering
        self.numbering_preserve = numbering_preserve
        self.number = 0
        self.caption_prefix_class = caption_prefix_class
        self.caption_class = caption_class
        self.content_class = content_class
        self.link_process = link_process
        self.caption_top = caption_top

        self._match_title = ""
        self._match_number = None

    def build_content_element(self, par, caption, replace=True):
        """Format the content element containing the caption"""
        attrib = par.attrib
        if replace:
            par.clear()
        par.tag = self.content_tag
        for k, v in attrib.items():
            par.set(k, v)

        if self.content_class:
            if "class" in attrib:
                par.set("class", self.content_class + " " + attrib["class"])
            else:
                par.set("class", self.content_class)
        if "id" not in attrib:
            par.set("id", "_{}-{}".format(self.name, self.get_number()))

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
                self.caption_prefix, self.get_number()
            )
            caption_prefix_span.tail = " {}".format(title)
        else:
            caption_prefix_span.text = "{}&nbsp;{}".format(
                self.caption_prefix, self.get_number()
            )
            caption_prefix_span.tail = ""
        if self.caption_prefix_class:
            caption_prefix_span.set("class", self.caption_prefix_class)
        return caption

    def matches(self, par):
        """
        Whether the element tree part matches the object to be captioned.
        This can be overriden by the subclasses.
        """
        self.reset_match()
        if par.text:
            match_caption = self._match_re.match(par.text)
            if match_caption is not None:
                return self.match_valid(match_caption.group("title"),
                                        match_caption.group("number"))
        return False

    def reset_match(self):
        """Resets the last found caption match data."""
        self._match_title = ""
        self._match_number = None

    def match_valid(self, title="", number=None):
        """
        Remember the determined number, title.
        Determines if the current match should not be skipped.
        """
        if title is not None:
            title = title.strip()
        valid = not self.caption_skip_empty or title
        if valid:
            self._match_title = title or ""
            try:
                self._match_number = int(number)
            except TypeError:
                pass
            except ValueError:
                pass
        return True

    def get_title(self):
        """Title of the matched figure. This can be overriden by the subclasses."""
        return self._match_title

    def get_number(self):
        """Number of the matched figure. This can be overriden by the subclasses."""
        if self.numbering_preserve and self._match_number is not None:
            return self._match_number
        return self.number

    def run(self, root):
        """Find and format all captions."""
        for par in root.findall("./p"):
            if not self.matches(par):
                continue
            self.number += 1
            title = self.get_title()
            caption = self.build_caption_element(title)
            self.build_content_element(par, caption)
            self.add_caption_to_content(par, caption)


class ListingCaptionTreeProcessor(CaptionTreeprocessor):
    name = "listing"
    content_tag = "div"

    def __init__(self, *args, **kwargs):
        super(ListingCaptionTreeProcessor, self).__init__(*args, **kwargs)


class CaptionExtension(Extension):
    # caption Extension

    def __init__(self, **kwargs):
        # Setup configs
        self.config = {
            "caption_prefix": [
                "Listing",
                "The text to show in front of the listing caption.",
            ],
            "caption_match_re": [
                r"^Listing\s*?(?P<number>\d*)\:\s*(?P<title>.*)",
                "The regexp used to match captions."
                "The group(number) can match a optional number."
                "The group(title) needs to match the title.",
            ],
            "caption_skip_empty": [
                False,
                "Dont create captions for empty titles."
            ],
            "numbering": [True, "Add the caption number to the prefix."],
            "numbering_preserve": [
                False,
                "Preserve matched numbers from caption match."
            ],
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

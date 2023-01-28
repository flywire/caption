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
from markdown import Extension

from caption.caption import CaptionTreeprocessor


class ImageCaptionTreeProcessor(CaptionTreeprocessor):
    name = "figure"
    content_tag = "figure"

    def __init__(
        self,
        md=None,
        caption_prefix="",
        numbering=True,
        caption_prefix_class=None,
        caption_class=None,
        content_class=None,
        strip_title=True,
    ):
        super(ImageCaptionTreeProcessor, self).__init__(
            md,
            caption_prefix,
            numbering,
            caption_prefix_class,
            caption_class,
            content_class
        )
        self.strip_title = strip_title

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
        super(ImageCaptionTreeProcessor, self).build_content_element(par)
        if self._a is not None:
            self._a.tail = "\n"
            par.append(self._a)
        else:
            self._img.tail = self._img.tail or "" + "\n"
            par.append(self._img)

    def build_caption_element(self, par, title):
        super(ImageCaptionTreeProcessor, self).build_caption_element(par, title)
        if self.strip_title and title:
            del self._img.attrib["title"]


class ImageCaptionExtension(Extension):
    # caption Extension

    def __init__(self, **kwargs):
        # Setup configs
        self.config = {
            "caption_prefix": [
                "Figure",
                "The text to show in front of the image caption.",
            ],
            "numbering": [True, "Add the caption number to the prefix."],
            "caption_prefix_class": [
                "",
                "CSS class to add to the caption prefix <span /> element.",
            ],
            "caption_class": ["", "CSS class to add to the caption element."],
            "content_class": ["", "CSS class to add to the content element."],
            "strip_title": [True, "Remove the title from the img tag."],
        }
        super(ImageCaptionExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.treeprocessors.register(
            ImageCaptionTreeProcessor(
                md,
                caption_prefix=self.getConfig("caption_prefix"),
                numbering=self.getConfig("numbering"),
                caption_prefix_class=self.getConfig("caption_prefix_class"),
                caption_class=self.getConfig("caption_class"),
                content_class=self.getConfig("content_class"),
                strip_title=self.getConfig("strip_title"),
            ),
            "figurecaptiontreeprocessor",
            8,
        )


def makeExtension(**kwargs):
    return ImageCaptionExtension(**kwargs)

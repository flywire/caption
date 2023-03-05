"""
caption - Manage markdown captions

Applying style and auto-numbering to Python-Markdown content.

https://github.com/flywire/caption
Copyright (c) 2020-2023 flywire
Copyright (c) 2023 sanzoghenzo
Copyright (c) 2023 Hendrik Polczynski
forked from yafg - https://git.sr.ht/~ferruck/yafg
Copyright (c) 2019-2020 Philipp Trommler

SPDX-License-Identifier: GPL-3.0-or-later
"""
from markdown import Extension

from .caption import CaptionTreeprocessor


class ImageCaptionTreeProcessor(CaptionTreeprocessor):
    name = "figure"
    content_tag = "figure"

    def __init__(self, *args, **kwargs):
        self.strip_title = kwargs.pop("strip_title", True)
        super(ImageCaptionTreeProcessor, self).__init__(*args, **kwargs)

    def reset_match(self):
        super(ImageCaptionTreeProcessor, self).reset_match()
        self._a = None
        self._img = None

    def matches(self, par):
        self.reset_match()
        self._img = par.find("./img")
        if self._img is None:
            self._a = par.find("./a")
            if self._a is not None:
                self._img = self._a.find("./img")

        if self._img is not None:
            return self.match_valid(self._img.get("title"))
        return False

    def build_content_element(self, par, caption, replace=True):
        super(ImageCaptionTreeProcessor, self).build_content_element(par, caption, replace=replace)
        if self._a is not None:
            self._a.tail = "\n"
            par.append(self._a)
        else:
            self._img.tail = self._img.tail or "" + "\n"
            par.append(self._img)

    def build_caption_element(self, title):
        caption = super(ImageCaptionTreeProcessor, self).build_caption_element(title)
        if self.strip_title and title:
            del self._img.attrib["title"]
        return caption


class ImageCaptionExtension(Extension):
    # caption Extension

    def __init__(self, **kwargs):
        # Setup configs
        self.config = {
            "caption_prefix": [
                "Figure",
                "The text to show in front of the image caption.",
            ],
            "caption_skip_empty": [
                False,
                "Dont create captions for empty titles."
            ],
            "numbering": [True, "Add the caption number to the prefix."],
            "caption_prefix_class": [
                "",
                "CSS class to add to the caption prefix <span /> element.",
            ],
            "caption_class": ["", "CSS class to add to the caption element."],
            "content_class": ["", "CSS class to add to the content element."],
            "strip_title": [True, "Remove the title from the img tag."],
            "caption_top": [False, "Put the caption at the top of the image."],
        }
        super(ImageCaptionExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.treeprocessors.register(
            ImageCaptionTreeProcessor(md, **self.getConfigs()),
            "figurecaptiontreeprocessor",
            8,
        )


def makeExtension(**kwargs):
    return ImageCaptionExtension(**kwargs)

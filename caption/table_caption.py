# caption - Manage markdown captions
#
# Copyright (c) 2020-2023 flywire
# Copyright (c) 2023 sanzoghenzo
# forked from yafg - https://git.sr.ht/~ferruck/yafg
# Copyright (c) 2019 Philipp Trommler
#
# SPDX-License-Identifier: GPL-3.0-or-later
from xml.etree import ElementTree

from markdown import Extension

from caption.caption import CaptionTreeprocessor


class TableCaptionTreeProcessor(CaptionTreeprocessor):
    name = "table"
    content_tag = "table"
    caption_tag = "caption"

    def matches(self, par):
        return par.text and par.text.startswith("Table: ")

    def get_title(self, par):
        return par.text[7:]

    def add_caption_to_content(self, content, caption):
        if not self.caption_top:
            caption.set("style", "caption-side:bottom")
        content.insert(0, caption)

    def run(self, root):
        """Find and format all captions."""
        root_iterator = iter(root)
        for child in root_iterator:
            if child.tag != "p" or not self.matches(child):
                continue
            next_item = next(root_iterator)
            if next_item.tag != self.content_tag:
                continue
            self.number += 1
            title = self.get_title(child)
            root.remove(child)
            caption = self.build_caption_element(title)
            self.build_content_element(next_item, caption, replace=False)
            self.add_caption_to_content(next_item, caption)


class TableCaptionExtension(Extension):
    # caption Extension

    def __init__(self, **kwargs):
        # Setup configs
        self.config = {
            "caption_prefix": [
                "Table",
                "The text to show in front of the table caption.",
            ],
            "numbering": [True, "Add the caption number to the prefix."],
            "caption_prefix_class": [
                "",
                "CSS class to add to the caption prefix <span /> element.",
            ],
            "caption_class": ["", "CSS class to add to the caption element."],
            "content_class": ["", "CSS class to add to the content element."],
            "caption_top": [True, "Put the caption at the top of the table."],
        }
        super(TableCaptionExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.treeprocessors.register(
            TableCaptionTreeProcessor(md, **self.getConfigs()),
            "tablecaptiontreeprocessor",
            8,
        )


def makeExtension(**kwargs):
    return TableCaptionExtension(**kwargs)

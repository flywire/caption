"""
caption - Manage markdown captions

Applying style and auto-numbering to Python-Markdown content.

https://github.com/flywire/caption
Copyright (c) 2020 flywire
forked from yafg - https://git.sr.ht/~ferruck/yafg
Copyright (c) 2019-2020 Philipp Trommler

SPDX-License-Identifier: GPL-3.0-or-later
"""

from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from xml.etree import ElementTree


class CaptionTreeprocessor(Treeprocessor):
    def __init__(
        # Make content types and attributes
        self,
        name="figure",
        caption_prefix=None,
        numbering=True,
        top_caption=True,
        caption_prefix_class=None,
        caption_class=None,
        content_class=None,
        id_prefix=None,
        link_process=None,
        content_tag=None,
        caption_tag="figcaption",
        prefix_tag="span",
        id=None,
    ):

        self.name = name
        if caption_prefix is not None:
            self.caption_prefix = caption_prefix
        else:
            self.caption_prefix = name.capitalize()
        self.numbering = numbering
        self.number = 0
        self.top_caption = top_caption
        self.caption_prefix_class = caption_prefix_class
        self.caption_class = caption_class
        self.content_class = content_class
        self.id_prefix = id_prefix
        self.link_process = link_process
        self.content_tag = (
            "div class={}".format(name) if content_tag is None else content_tag
        )
        self.caption_tag = caption_tag
        self.prefix_tag = prefix_tag
        self.id = "_{}-".format(name) if id is None else id

    @staticmethod
    def match_children(par):
        # Find images in links
        a = None
        img = par.find("./img")
        if img is None:
            a = par.find("./a")
            if a is not None:
                img = a.find("./img")
                if img is None:
                    a = None
        return img, a

    def build_content_element(self, par, type_):
        # Format the content element containing the caption
        attrib = par.attrib
        par.clear()
        par.tag = type_.content_tag
        for k, v in attrib.items():
            par.set(k, v)
        if type_.content_class:
            par.set("class", type_.content_class)
        par.set("id", "_{}-{}".format(type_.name, type_.number))
        par.text = "\n"
        par.tail = "\n"

    def build_caption_element(self, par, title, type_):
        # Format the caption
        caption = ElementTree.SubElement(par, type_.caption_tag)
        if type_.caption_class:
            caption.set("class", type_.caption_class)
        if type_.numbering:
            caption_prefix_span = ElementTree.SubElement(caption, type_.prefix_tag)
            if title:
                caption_prefix_span.text = "{}&nbsp;{}:".format(
                    type_.caption_prefix, type_.number
                )
                caption_prefix_span.tail = " {}".format(title)
            else:
                caption_prefix_span.text = "{}&nbsp;{}".format(
                    type_.caption_prefix, type_.number
                )
                caption_prefix_span.tail = ""
            if type_.caption_prefix_class:
                caption_prefix_span.set("class", type_.caption_prefix_class)
        else:
            caption.text = title

        caption.tail = "\n"

    def run(self, root):
        # Find and format all captions
        # Define content types and attributes
        figure = CaptionTreeprocessor(
            top_caption=False,
            content_tag="figure",
            link_process=self.link_process or "strip_title",
            caption_class=self.caption_class,
            caption_prefix=self.caption_prefix,
            caption_prefix_class=self.caption_prefix_class,
            content_class=self.content_class,
            numbering=self.numbering,
        )
        table = CaptionTreeprocessor(
            name="table",
            content_tag="table",
            caption_tag="caption",
            link_process=self.link_process or "line_2_caption",
        )
        listing = CaptionTreeprocessor(name="listing")
        for par in root.findall("./p"):
            if par.text and par.text.startswith("Table: "):
                obj = table
                title = par.text[len("Table: ") :]
            elif par.text and par.text.startswith("Listing: "):
                obj = listing
                title = par.text[len("Listing: ") :]
            else:
                img, a = CaptionTreeprocessor.match_children(par)
                if img is None:
                    continue
                obj = figure

            obj.number += 1
            self.build_content_element(par, obj)

            if obj.name == "figure":
                if a is not None:
                    a.tail = "\n"
                    par.append(a)
                else:
                    if img.tail is None:
                        img.tail = "\n"
                    else:
                        img.tail += "\n"
                    par.append(img)
                title = img.get("title")

            self.build_caption_element(par, title, obj)
            if obj.name == "figure" and obj.link_process == "strip_title" and title:
                del img.attrib["title"]


class CaptionExtension(Extension):
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
            "link_process": ["", "Some content types support linked processes."],
        }
        super(CaptionExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        # Add pieces to Markdown
        md.treeprocessors.register(
            CaptionTreeprocessor(
                md,
                caption_prefix=self.getConfig("caption_prefix"),
                numbering=self.getConfig("numbering"),
                caption_prefix_class=self.getConfig("caption_prefix_class"),
                caption_class=self.getConfig("caption_class"),
                content_class=self.getConfig("content_class"),
                link_process=self.getConfig("link_process"),
            ),
            "captiontreeprocessor",
            8,
        )


def makeExtension(**kwargs):
    return CaptionExtension(**kwargs)

'''
caption - Manage markdown captions

Applying style and auto-numbering to Python-Markdown content.

https://github.com/flywire/caption
Copyright (c) 2020 flywire
forked from yafg - https://git.sr.ht/~ferruck/yafg
Copyright (c) 2019-2020 Philipp Trommler

SPDX-License-Identifier: GPL-3.0-or-later
'''

from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from xml.etree import ElementTree


class captionTreeprocessor(Treeprocessor):
    def __init__(
        # Make content types and attributes
        self,
        name = "figure",
        caption_prefix = None,
        numbering = True,
        top_caption = True,
        caption_prefix_class = None,
        caption_class = None,
        content_class = None,
        id_prefix = None,
        link_process = None,
        content_tag = None,
        caption_tag = "figcaption",
        prefix_tag = "span",
        id = None
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
        if content_tag is not None:
           self.content_tag = content_tag
        else:
           self.content_tag = "div class={}".format(name)
        self.caption_tag = caption_tag
        self.prefix_tag = prefix_tag
        if id is not None:
           self.id = id
        else:
           self.id = "_{}-".format(name)

    @staticmethod
    def matchChildren(par):
        # Find images in links
        a = None
        img = par.find("./img")
        if img is None:
            a = par.find("./a")
            if a is not None:
                img = a.find("./img")
                if img is None:
                    a = None
        return (img, a)

    def buildContentElement(self, par, Type):
        # Format the content element containing the caption
        attrib = par.attrib
        par.clear()
        par.tag = Type.content_tag
        for k, v in attrib.items():
            par.set(k, v)
        if Type.content_class is not None:
            par.set("class", Type.content_class)
        par.set("id", "_{}-{}".format(Type.name, Type.number))
        par.text = "\n"
        par.tail = "\n"

    def buildCaptionElement(self, par, title, Type):
        # Format the caption
        caption = ElementTree.SubElement(par, Type.caption_tag)
        if Type.caption_class:
            caption.set("class", Type.caption_class)
        if Type.numbering:
            caption_prefixSpan = ElementTree.SubElement(caption, Type.prefix_tag)
            if title:
                caption_prefixSpan.text = "{}&nbsp;{}:".format(Type.caption_prefix, Type.number)
                caption_prefixSpan.tail = " {}".format(title)
            else:
                caption_prefixSpan.text = "{}&nbsp;{}".format(Type.caption_prefix, Type.number)
                caption_prefixSpan.tail = ""
            if Type.caption_prefix_class is not None:
                caption_prefixSpan.set("class", Type.caption_prefix_class)
        else:
            caption.text = title

        caption.tail = "\n"

    def run(self, root):
        # Find and format all captions
        # Define content types and attributes
        Figure = captionTreeprocessor(
            top_caption = False,
            content_tag = "figure",
            link_process = "strip_title",
            caption_class=self.caption_class)
        Table = captionTreeprocessor(
            name = "table",
            content_tag = "table",
            caption_tag = "caption",
            link_process = "line_2_caption")
        Listing = captionTreeprocessor(
            name = "listing")	
        for par in root.findall("./p"):
            if par.text and par.text.startswith("Table: "):
                Type = Table
                title = par.text[len("Table: "):]
            elif par.text and par.text.startswith("Listing: "):
                Type = Listing
                title = par.text[len("Listing: "):]
            else:
                img, a = captionTreeprocessor.matchChildren(par)
                if img is None:
                    continue
                Type = Figure

            Type.number += 1
            self.buildContentElement(par, Type)

            if Type.name == "figure":
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

            self.buildCaptionElement(par, title, Type)
            if Type.name == "figure" and Type.link_process == "strip_title" and title:
                del img.attrib["title"]


class captionExtension(Extension):
    # caption Extension

    def __init__(self, **kwargs):
        # Setup configs
        self.config = {
            "caption_prefix" : ["Figure", "The text to show in front of the image caption."],
            "numbering" : [True, "Add the caption number to the prefix."],
            "caption_prefix_class" : ["", "CSS class to add to the caption prefix <span /> element."],
            "caption_class" : ["", "CSS class to add to the caption element."],
            "content_class" : ["", "CSS class to add to the content element."],
            "link_process" : ["", "Some content types support linked processes."],
        }
        super(captionExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        # Add pieces to Markdown
        md.treeprocessors.register(
            captionTreeprocessor(
                md,
                caption_prefix=self.getConfig("caption_prefix"),
                numbering=self.getConfig("numbering"),
                caption_prefix_class=self.getConfig("caption_prefix_class"),
                caption_class=self.getConfig("caption_class"),
                content_class=self.getConfig("content_class"),
                link_process=self.getConfig("link_process"),
            ),
            "captiontreeprocessor",
            8)

def makeExtension(**kwargs):
    return captionExtension(**kwargs)

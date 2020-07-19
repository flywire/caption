# caption - Manage markdown captions
# https://github.com/flywire/caption
# Copyright (c) 2020 flywire
# forked from yafg - https://git.sr.ht/~ferruck/yafg
# Copyright (c) 2019 Philipp Trommler
#
# SPDX-License-Identifier: GPL-3.0-or-later
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from xml.etree import ElementTree

class captionTreeprocessor(Treeprocessor):
    def __init__(
        self,
        md,
        type = "figure",
        caption_prefix = None,
        numbering = True,
        top_caption = True,
        caption_prefix_class = None,
        caption_class = None,
        content_class = None,
        id_prefix = None,
        special_process = None,
        content_tag = None,
        caption_tag = "figcaption",
        prefix_tag = "span",
        linked_process = None,
        id = None
        ):

        self.type = type
        if caption_prefix is not None:
            self.caption_prefix = caption_prefix
        else:
            self.caption_prefix = type.capitalize()
        self.numbering = numbering
        self.caption_number = 0
        self.top_caption = top_caption
        self.caption_prefix_class = caption_prefix_class
        self.caption_class = caption_class
        self.content_class = content_class
        self.id_prefix = id_prefix
        self.special_process = special_process
        if content_tag is not None:
           self.content_tag = content_tag
        else:
           self.content_tag = "div class-{}:".format(type)
        self.caption_tag = caption_tag
        self.prefix_tag = prefix_tag
        self.linked_process = linked_process
        if id is not None:
           self.id = id
        else:
           self.id = "_{}-".format(type)

# +   *type : listing
# + ***prefix : Listing
# + ***numbering : True
#     *top_caption : True
# + ***caption_prefix_class : None
# + ***caption_class : None
# + ***content_class : None
# +  **id_prefix : None
# + ***special_process : None
#    **content_tag : div class-listing:
#    **caption_tag : figcaption
#    **prefix_tag : span
#     *linked_process : None
#    **id : _listing-
#
#   *** setting, ** coded, * logic

# Figure = Content(
#     top_caption = False,
#     content_tag = "<figure>",
#     linked_process = "strip_title")
# 
# Table = Content(
#     type = "table",
#     content_tag = "<table>",
#     caption_tag = "<caption>",
#     linked_process = "line_2_caption")
# 
# Listing = Content(
#     type = "listing")

    @staticmethod
    def matchChildren(par):
        a = None
        img = par.find("./img")
        if img is None:
            a = par.find("./a")
            if a is not None:
                img = a.find("./img")
                if img is None:
                    a = None
        return (img, a)

    def buildContentElement(self, par):
        attrib = par.attrib
        par.clear()
        par.tag = "figure"
        for k, v in attrib.items():
            par.set(k, v)
        par.set("id", "_caption-{}".format(self.caption_number))
        par.text = "\n"
        par.tail = "\n"

    def buildCaptionElement(self, par, title):
        caption = ElementTree.SubElement(par, self.caption_tag)
        if self.numbering:
            caption_prefixSpan = ElementTree.SubElement(caption, self.prefix_tag)
            caption_prefixSpan.text = "{}&nbsp;{}:".format(self.caption_prefix, self.caption_number)
            caption_prefixSpan.tail = " {}".format(title)
        else:
            caption.text = title
        caption.tail = "\n"


    def run(self, root):
        for par in root.findall("./p"):
            if par.text and par.text.startswith("Table: "):
                title = par.text[len("Table: "):]
                self.caption_number += 1
                self.buildContentElement(par)
            elif par.text and par.text.startswith("Listing: "):
                title = par.text[len("Listing: "):]
                self.caption_number += 1
                self.buildContentElement(par)
            else:
                img, a = captionTreeprocessor.matchChildren(par)
                if img is None:
                    continue
                self.caption_number += 1
                self.buildContentElement(par)
                if a is not None:
                    a.tail = "\n"
                    par.append(a)
                    title = img.get("title")
                else:
                    if img.tail is None:
                        img.tail = "\n"
                    else:
                        img.tail += "\n"
                    par.append(img)
                    title = img.get("title")
            self.buildCaptionElement(par, title)

class captionExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            "caption_prefix" : ["Figure", "The text to show in front of the image caption."],
            "numbering" : [True, "Add the caption number to the prefix."],
            "caption_prefix_class" : ["", "CSS class to add to the caption prefix <span /> element."],
            "caption_class" : ["", "CSS class to add to the caption element."],
            "content_class" : ["", "CSS class to add to the content element."],
#            "stripTitle" : [False, "Strip the title from the <img />."],
        }
        super(captionExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.treeprocessors.register(
            captionTreeprocessor(
                md,
                caption_prefix=self.getConfig("caption_prefix"),
                numbering=self.getConfig("numbering"),
                caption_prefix_class=self.getConfig("caption_prefix_class"),
                caption_class=self.getConfig("caption_class"),
                content_class=self.getConfig("content_class"),
 #               stripTitle=self.getConfig("stripTitle"),
            ),
            "captiontreeprocessor",
            8)

def makeExtension(**kwargs):
    return captionExtension(**kwargs)

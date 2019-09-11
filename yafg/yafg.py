# yafg: Yet Another Figure Generator
#
# Copyright (c) 2019 Philipp Trommler
#
# SPDX-License-Identifier: GPL-3.0-or-later
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from xml.etree import ElementTree

class YafgTreeprocessor(Treeprocessor):
    def __init__(self, md, stripTitle):
        self.md = md
        self.stripTitle = stripTitle

    def run(self, root):
        for par in root.findall("./p[img]"):
            attrib = par.attrib
            img = par.find("img")
            title = img.get("title")

            par.clear()
            par.tag = "figure"
            for k, v in attrib.items():
                par.set(k, v)
            par.text = "\n"

            img.tail = "\n"
            if self.stripTitle:
                del img.attrib["title"]
            par.append(img)

            figcaption = ElementTree.SubElement(par, "figcaption")
            figcaption.text = title
            figcaption.tail = "\n"

class YafgExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {"stripTitle" : [False, "Strip the title from the <img />."]}
        super(YafgExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.treeprocessors.register(
                YafgTreeprocessor(md, stripTitle = self.getConfig("stripTitle")),
                "yafgtreeprocessor",
                15)

def makeExtension(**kwargs):
    return YafgExtension(**kwargs)

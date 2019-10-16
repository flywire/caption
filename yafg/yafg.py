# yafg: Yet Another Figure Generator
#
# Copyright (c) 2019 Philipp Trommler
#
# SPDX-License-Identifier: GPL-3.0-or-later
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from xml.etree import ElementTree

class YafgTreeprocessor(Treeprocessor):
    def __init__(self, md, stripTitle, figureClass, figcaptionClass):
        self.md = md
        self.stripTitle = stripTitle
        self.figureClass = figureClass
        self.figcaptionClass = figcaptionClass

    def run(self, root):
        for par in root.findall("./p[img]"):
            attrib = par.attrib
            img = par.find("img")
            title = img.get("title")

            par.clear()
            par.tag = "figure"
            for k, v in attrib.items():
                par.set(k, v)
            if self.figureClass is not "":
                par.set("class", self.figureClass)
            par.text = "\n"

            img.tail = "\n"
            if self.stripTitle:
                del img.attrib["title"]
            par.append(img)

            figcaption = ElementTree.SubElement(par, "figcaption")
            if self.figcaptionClass is not "":
                figcaption.set("class", self.figcaptionClass)
            figcaption.text = title
            figcaption.tail = "\n"

class YafgExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
                "stripTitle" : [False, "Strip the title from the <img />."],
                "figureClass" : ["", "CSS class to add to the <figure /> element."],
                "figcaptionClass" : ["", "CSS class to add to the <figcaption /> element."],
        }
        super(YafgExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.treeprocessors.register(
                YafgTreeprocessor(
                    md,
                    stripTitle=self.getConfig("stripTitle"),
                    figureClass=self.getConfig("figureClass"),
                    figcaptionClass=self.getConfig("figcaptionClass"),
                ),
                "yafgtreeprocessor",
                15)

def makeExtension(**kwargs):
    return YafgExtension(**kwargs)

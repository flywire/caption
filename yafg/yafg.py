# yafg: Yet Another Figure Generator
#
# Copyright (c) 2019 Philipp Trommler
#
# SPDX-License-Identifier: GPL-3.0-or-later
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from xml.etree import ElementTree

class YafgTreeprocessor(Treeprocessor):
    def __init__(
            self,
            md,
            stripTitle,
            figureClass,
            figcaptionClass,
            figureNumbering,
            figureNumberClass):
        self.md = md
        self.stripTitle = stripTitle
        self.figureClass = figureClass
        self.figcaptionClass = figcaptionClass
        self.figureNumbering = figureNumbering
        self.figureNumber = 0
        self.figureNumberClass = figureNumberClass

    def run(self, root):
        for par in root.findall("./p[img]"):
            self.figureNumber += 1

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

            if self.figureNumbering:
                figureNumberSpan = ElementTree.SubElement(figcaption, "span")
                figureNumberSpan.text = "Figure&nbsp;{}:".format(self.figureNumber)
                figureNumberSpan.tail = " {}".format(title)
                if self.figureNumberClass is not "":
                    figureNumberSpan.set("class", self.figureNumberClass)
            else:
                figcaption.text = title

            figcaption.tail = "\n"

class YafgExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
                "stripTitle" : [False, "Strip the title from the <img />."],
                "figureClass" : ["", "CSS class to add to the <figure /> element."],
                "figcaptionClass" : ["", "CSS class to add to the <figcaption /> element."],
                "figureNumbering" : [False, "Show the figure number in front of the image caption."],
                "figureNumberClass" : ["", "CSS class to add to the figure number <span /> element."],
        }
        super(YafgExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.treeprocessors.register(
                YafgTreeprocessor(
                    md,
                    stripTitle=self.getConfig("stripTitle"),
                    figureClass=self.getConfig("figureClass"),
                    figcaptionClass=self.getConfig("figcaptionClass"),
                    figureNumbering=self.getConfig("figureNumbering"),
                    figureNumberClass=self.getConfig("figureNumberClass"),
                ),
                "yafgtreeprocessor",
                15)

def makeExtension(**kwargs):
    return YafgExtension(**kwargs)

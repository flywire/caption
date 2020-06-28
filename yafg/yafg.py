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
            captionClass,
            capcaptionClass,
            captionNumbering,
            captionNumberClass,
            captionPrefix):
        self.md = md
        self.stripTitle = stripTitle
        self.captionClass = captionClass
        self.capcaptionClass = capcaptionClass
        self.captionNumbering = captionNumbering
        self.captionNumber = 0
        self.captionNumberClass = captionNumberClass
        self.captionPrefix = captionPrefix

    def run(self, root):
        for par in root.findall("./p[img]"):
            self.captionNumber += 1

            attrib = par.attrib
            img = par.find("img")
            title = img.get("title")

            par.clear()
            par.tag = "figure"

            # Allow caption before or after

            # Object starts here
            for k, v in attrib.items():
                par.set(k, v)
            if self.captionClass is not "":
                par.set("class", self.captionClass)
            par.text = "\n"

            img.tail = "\n"
            # Images only
            if self.stripTitle:
                del img.attrib["title"]
            par.append(img)

            # Caption starts here
            capcaption = ElementTree.SubElement(par, "capcaption")
            if self.capcaptionClass is not "":
                capcaption.set("class", self.capcaptionClass)

            if self.captionNumbering:
                captionNumberSpan = ElementTree.SubElement(capcaption, "span")
                captionNumberSpan.text = "{}&nbsp;{}:".format(self.captionPrefix, self.captionNumber)
                captionNumberSpan.tail = " {}".format(title)
                if self.captionNumberClass is not "":
                    captionNumberSpan.set("class", self.captionNumberClass)
            else:
                capcaption.text = title

            capcaption.tail = "\n"

class YafgExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
                "stripTitle" : [False, "Strip the title from the <img />."],
                "captionClass" : ["", "CSS class to add to the <caption /> element."],
                "capcaptionClass" : ["", "CSS class to add to the <capcaption /> element."],
                "captionNumbering" : [False, "Show the caption number in front of the image caption."],
                "captionNumberClass" : ["", "CSS class to add to the caption number <span /> element."],
                "captionPrefix" : ["Figure", "The text to show at the front of the caption."],
        }
        super(YafgExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.treeprocessors.register(
                YafgTreeprocessor(
                    md,
                    stripTitle=self.getConfig("stripTitle"),
                    captionClass=self.getConfig("captionClass"),
                    capcaptionClass=self.getConfig("capcaptionClass"),
                    captionNumbering=self.getConfig("captionNumbering"),
                    captionNumberClass=self.getConfig("captionNumberClass"),
                    captionPrefix=self.getConfig("captionPrefix"),
                ),
                "yafgtreeprocessor",
                15)

def makeExtension(**kwargs):
    return YafgExtension(**kwargs)

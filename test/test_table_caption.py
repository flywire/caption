# caption - Manage markdown captions
#
# Copyright (c) 2020-2023 flywire
# Copyright (c) 2023 sanzoghenzo
# forked from yafg - https://git.sr.ht/~ferruck/yafg
# Copyright (c) 2019 Philipp Trommler
#
# SPDX-License-Identifier: GPL-3.0-or-later
import markdown

from caption import TableCaptionExtension


def test_empty_input():
    in_string = ""
    out_string = markdown.markdown(in_string, extensions=[TableCaptionExtension()])
    assert out_string == in_string


def test_no_table():
    in_string = """\
This is a test text.

It contains multiple paragraphs as well as [links](https://example.com).

* Itemize
* is
* used,
* as well.

# This is a headline.

Nothing should change here whilst using caption."""
    expected_string = markdown.markdown(in_string)
    out_string = markdown.markdown(in_string, extensions=[TableCaptionExtension()])
    assert out_string == expected_string


BASE_MD_TABLE = """\
Table: Example with heading, two columns and a row

| Syntax      | Description |
| ----------- | ----------- |
| Header      | Title       |
| Paragraph   | Text        |
"""


TABLE_INNER_CONTENT = """<thead>
<tr>
<th>Syntax</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>Header</td>
<td>Title</td>
</tr>
<tr>
<td>Paragraph</td>
<td>Text</td>
</tr>
</tbody>"""


def test_defaults():
    expected_string = """\
<table id="_table-1">
<caption><span>Table&nbsp;1:</span> Example with heading, two columns and a row</caption>
{}
</table>""".format(TABLE_INNER_CONTENT)
    out_string = markdown.markdown(BASE_MD_TABLE, extensions=["tables", TableCaptionExtension()])
    assert out_string == expected_string


def test_bottom_caption():
    expected_string = """\
<table id="_table-1">
<caption style="caption-side:bottom"><span>Table&nbsp;1:</span> Example with heading, two columns and a row</caption>
{}
</table>""".format(TABLE_INNER_CONTENT)
    out_string = markdown.markdown(BASE_MD_TABLE, extensions=["tables", TableCaptionExtension(caption_top=False)])
    assert out_string == expected_string


def test_content_class():
    expected_string = """\
<table class="testclass" id="_table-1">
<caption><span>Table&nbsp;1:</span> Example with heading, two columns and a row</caption>
{}
</table>""".format(TABLE_INNER_CONTENT)
    out_string = markdown.markdown(BASE_MD_TABLE, extensions=["tables", TableCaptionExtension(content_class="testclass")])
    assert out_string == expected_string


def test_caption_class():
    expected_string = """\
<table id="_table-1">
<caption class="testclass"><span>Table&nbsp;1:</span> Example with heading, two columns and a row</caption>
{}
</table>""".format(TABLE_INNER_CONTENT)
    out_string = markdown.markdown(BASE_MD_TABLE, extensions=["tables", TableCaptionExtension(caption_class="testclass")])
    assert out_string == expected_string


def test_no_numbering():
    expected_string = """\
<table id="_table-1">
<caption>Example with heading, two columns and a row</caption>
{}
</table>""".format(TABLE_INNER_CONTENT)
    out_string = markdown.markdown(BASE_MD_TABLE, extensions=["tables", TableCaptionExtension(numbering=False)])
    assert out_string == expected_string


def test_caption_prefix_class():
    expected_string = """\
<table id="_table-1">
<caption><span class="testclass">Table&nbsp;1:</span> Example with heading, two columns and a row</caption>
{}
</table>""".format(TABLE_INNER_CONTENT)
    out_string = markdown.markdown(BASE_MD_TABLE, extensions=["tables", TableCaptionExtension(caption_prefix_class="testclass")])
    assert out_string == expected_string


def test_caption_prefix():
    expected_string = """\
<table id="_table-1">
<caption><span>Tabula&nbsp;1:</span> Example with heading, two columns and a row</caption>
{}
</table>""".format(TABLE_INNER_CONTENT)
    out_string = markdown.markdown(BASE_MD_TABLE, extensions=["tables", TableCaptionExtension(caption_prefix="Tabula")])
    assert out_string == expected_string

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


def test_simple_table():
    in_string = """\
Table: Example with heading, two columns and a row

| Syntax      | Description |
| ----------- | ----------- |
| Header      | Title       |
| Paragraph   | Text        |
"""
    expected_string = """\
<table id="_table-1">
<caption><span>Table&nbsp;1:</span> Example with heading, two columns and a row</caption>
<thead>
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
</tbody>
</table>"""
    out_string = markdown.markdown(in_string, extensions=["tables", TableCaptionExtension()])
    assert out_string == expected_string

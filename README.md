# caption - manages markdown captions

*caption* manages captions by applying style and auto-numbering to markdown content.
It works on Figures, Tables and Other content such as Listings but is flexible and
should work for nearly any content.

*caption* is a fork of [yafg](https://git.sr.ht/~ferruck/yafg) - yet another
figure generator plugin for Python's Markdown. It's written and tested with
Python 2.7 and Python 3.6 as well as Markdown 3.1.1, but aims at supporting as
many versions as possible. If you encounter any problems with *caption* please
raise an [issue](https://github.com/flywire/caption/issues), or use the profile
contact details.

The functionality is split into three separate `python-maskdown` plugins:

- `image_captions` for images
- `table_captions` for tables
- `caption` for general listings.

## `image_captions`

It uses the `title` attribute given to an image within Markdown to generate a
`<figure>` environment with a `<figcaption>` containing the `title`'s text,
e.g.:

```markdown
![Alt text](/path/to/image.png "This is the title of the image.")
```

becomes

```html
<figure id="_figure-1">
<img alt="Alt text" src="/path/to/image.png" />
<figcaption><span>Figure&nbsp;1:</span> Captioned figure</figcaption>
</figure>
```

## `table_captions`

A paragraph starting with "Table" before a table is turned into a `caption`:

```markdown
Table: Example with heading, two columns and a row

| Syntax      | Description |
| ----------- | ----------- |
| Header      | Title       |
| Paragraph   | Text        |
```

becomes

```html
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
</table>
```

## `caption`

Generic listings captioning is supported, using the "Listing: " prefix:

```markdown
Listing: Example listing
```

becomes

```html
<caption><span>Listing&nbsp;1:</span> Example listing</caption>
```

## How?

### Install

*caption* can be installed via `pip3 install git+https://github.com/flywire/caption`

### Standard Usage

Python markdown extensions are incorporated into other applications.

### MkDocs

MkDocs users can add *caption* to their generator process by adding it to the
`mkdocs.yml` `markdown_extensions` section:

```yaml
# ...
markdown_extensions:
  - image_captions:
      numbering: true
  - table_captions:
      numbering: true
      caption_top: false
  - caption
# ...
```

### Python

Python will parse input to Markdown with *caption* as follows:

```python
import markdown
from caption import CaptionExtension, ImageCaptionExtension, TableCaptionExtension

# ...

outputString = markdown.markdown(
    input_string, extensions=[
        CaptionExtension(numbering=False),
        ImageCaptionExtension(),
        TableCaptionExtension(),
    ]
)
```

### Options

Currently supported options are listed below:

* `caption_prefix`:

    The text to show at the front of the caption. A final non-breaking space
    is inserted between the content of `caption_prefix` and the actual figure
    number.

* `numbering`:

    Adds a caption number like "Figure 1:" in front of the caption. It's
	wrapped in a `<span />` for easier styling.

* `content_class`:

    The CSS class to add to the generated `<content />` element.

* `caption_class`:

    The CSS class to add to the generated `<caption />` element.

* `caption_prefix_class`:

    The CSS class to add to the `<span />` element generated for the caption prefix.

* `caption_top`:

    Whether the caption should be on the top of the element.

The default values for each type of content is synthesised in the following table:

| Config                 | Image   | Table   | Other     |
|------------------------|---------|---------|-----------|
| `caption_prefix`       | "Image" | "Table" | "Listing" |
| `numbering`            | False   | False   | False     |
| `content_class`        | -       | -       | -         |
| `caption_class`        | -       | -       | -         |
| `caption_prefix_class` | -       | -       | -         |
| `caption_top`          | False   | True    | True      |

## Why?

Captions are used on a range of content, not just figures. For figures, 
yafg arose from the dissatisfaction with the existing solutions, namely:

* [markdown\_captions](https://github.com/evidlo/markdown_captions) which uses
  the `alt` attribute for the `<figcaption>`.
* [markdown-figcap](https://github.com/funk1d/markdown-figcap) which uses a
  cryptic syntax that doesn't integrate well into Markdown, IMHO.
* [figureAltCaption](https://github.com/jdittrich/figureAltCaption) which
  cannot handle multi-line descriptions and uses the `alt` attribute for the
  `<figcaption>`.

Using the `alt` attribute to fill the `<figcaption>` is not correct as described
in the standard (https://www.w3.org/wiki/Html/Elements/img).

> [...] the alternative text is a replacement for the image, not a description
> [...]

for the most common case of a text accompanied by an augmenting image. It should
be used for an exact reproduction of what can be seen on the image for those who
cannot see it, for example because they're blind or their internet connection is
too slow. A figure's caption in turn should provide a description helping to
understand the content of the image.

The `title` attribute on the other hand should contain "advisory information
associated with the element ([W3C Core Attribute
List](https://www.w3.org/wiki/Html/Attributes/_Global)). This is rather vague
and often used by browser vendors to show tooltips containing the title. Since
tooltips are highly problematic for a11y reasons and the browser support varies,
"[r]elying on the title attribute is currently discouraged" ([HTML Living
Standard](https://html.spec.whatwg.org/multipage/dom.html#the-title-attribute)).
This makes it an ideal candidate to store the wanted `figcaption` inside of the
standard Markdown syntax.

## CSS

*caption* fully supports CSS (Cascading Style Sheets) by adding tags to style
your content. CSS can be placed against the image eg {: style="height:200px"},
in the settings eg: {: style="width: 100%"} or in a CSS file linked in the HTML 
eg <link rel="stylesheet" href="styles.css">.

```css
figcaption span:first-child {
    font-weight: bold;
}
```
 There are further examples in the [wiki](https://github.com/flywire/caption/wiki).

## Customisable

If the settings aren't flexible enough the source code can be changed and
reinstalled. Many of the settings are easily identifiable in the source code
and the the [wiki](https://github.com/flywire/caption/wiki) has build instructions.

## License

*caption* has been published under a GPL 3.0 or later license. See the `LICENSE`
file for more information.

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

A new markdown syntax is added for tables and other content which requires 
lines to start with "Table: " or "Listing: " respectively.

## How?

### Install

*caption* can be installed via `pip3 install git+https://github.com/flywire/caption`

### Standard Usage

Python markdown extensions are incorporated into other applications.

### MkDocs

MkDocs users can add *caption* to their generator process by adding it to the
`mkdocs.yml` `markdown_extensions` section:

```python
site_name: captionTest
# theme:
#    name: material
# extra_css: [extra.css]
markdown_extensions:
    - caption:
        numbering: false
nav:
    - Home: index.md
```

### Python

Python will parse input to Markdown with *caption* as follows:

```python
import markdown
from caption import CaptionExtension

# ...

outputString = markdown.markdown(
    input_string, extensions=[CaptionExtension(numbering=False)]
)
```

### Options

Currently supported options are listed below:

* `captionPrefix` (default: `"Figure"`):

    The text to show at the front of the caption. A final non-breaking space
    is inserted between the content of `captionPrefix` and the actual figure
    number.

* `numbering` (default: `True`):

    Adds a caption number like "Figure 1:" in front of the caption. It's
	wrapped in a `<span />` for easier styling.

* `content_class` (default: `""`):

    The CSS class to add to the generated `<content />` element.

* `caption_class` (default: `""`):

    The CSS class to add to the generated `<caption />` element.

* `caption_prefix_class` (default: `""`):

    The CSS class to add to the `<span />` element generated for the caption prefix.

* `link_process` (default: ""):

    Content types may have a built-in link_process, for example figures have
	"strip_title" which removes the original `title` attribute from the `<img />`
	element. Its usage is discouraged and this format my be preferred.

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

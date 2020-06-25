# yafg - Yet Another Figure Generator

*yafg* is yet another figure generator plugin for Python's Markdown. It's
written and tested with Python 2.7 and Python 3.6 as well as Markdown 3.1.1, but
aims at supporting as many versions as possible. If you encounter any problems
with the given versions or find yourself using *yafg* without problems with any
others, please give me a hint using the e-mail address listed below.

It uses the `title` attribute given to an image within Markdown to generate a
`<figure>` environment with a `<figcaption>` containing the `title`'s text,
e.g.:

```markdown
![Alt text](/path/to/image.png "This is the title of the image.")
```

becomes

```html
<figure>
<img alt="Alt text" src="/path/to/image.png" title="This is the title of the image." />
<figcaption>This is the title of the image.</figcaption>
</figure>
```

## How?

### Install

*yafg* can be installed via PyPI using:

```
pip install yafg
```

### Standard Usage

When parsing your input, you can add *yafg* to Markdown as follows:

```python
import yafg

# ...

outputString = markdown.markdown(inputString, extensions = [yafg.YafgExtension(stripTitle=False)])
```

### Pelican

Pelican users can add *yafg* to their generator process by adding it to the
`MARKDOWN` variable in the `pelicanconf.py` as follows:

```python
MARKDOWN = {
    'extensions_configs': {
        'yafg': {
            'stripTitle': 'False',
        },
    },
}
```

### Options

Currently supported options are listed below:

* `stripTitle` (default: `False`):

    Removes the original `title` attribute from the `<img />` element. Since its
    usage is discouraged anyways (see below), this may be an option worth
    considering.

* `figureClass` (default: `""`):

    The CSS class to add to the generated `<figure />` element.

* `figcaptionClass` (default: `""`):

    The CSS class to add to the generated `<figcaption />` element.

* `figureNumbering` (default: `False`):

    Adds a figure number like "Figure 1:" in front of the caption. It's wrapped
    in a `<span />` for easier styling.

* `figureNumberClass` (default: `""`):

    The CSS class to add to the `<span />` element generated for the figure
    number.

* `figureNumberText` (default: `"Figure"`):

    The text to show in front of the figure number. A final non-breaking space
    is inserted between the content of `figureNumberText` and the actual figure
    number.

## Why?

yafg arose from the dissatisfaction with the existing solutions, namely:

* [markdown\_captions](https://github.com/evidlo/markdown_captions) which uses
  the `alt` attribute for the `<figcaption>`.
* [markdown-figcap](https://github.com/funk1d/markdown-figcap) which uses a
  cryptic syntax that doesn't integrate well into Markdown, IMHO.
* [figureAltCaption](https://github.com/jdittrich/figureAltCaption) which
  cannot handle multi-line descriptions and uses the `alt` attribute for the
  `<figcaption>`.

Using the `alt` attribute to fill the `<figcaption>` is not correct, because [as
the standard states](https://www.w3.org/wiki/Html/Elements/img)

> [...] the alternative text is a replacement for the image, not a description
> [...]

for the most common case of a text accompanied by an augmenting image. It should
be used for an exact reproduction of what can be seen on the image for those who
cannot see it, for example because they're blind or their internet connection is
too slow. A figure's caption in turn should provide a description helping to
understand the content of the image.

The `title` attribute on the other hand should contain "[a]dvisory information
associated with the element ([W3C Core Attribute
List](https://www.w3.org/wiki/Html/Attributes/_Global)). This is rather vague
and often used by browser vendors to show tooltips containing the title. Since
tooltips are highly problematic for a11y reasons and the browser support varies,
"[r]elying on the title attribute is currently discouraged" ([HTML Living
Standard](https://html.spec.whatwg.org/multipage/dom.html#the-title-attribute)).
This makes it an ideal candidate to store the wanted `figcaption` inside of the
standard Markdown syntax.

## Author

*yafg* has been written by:

* Philipp Trommler <yafg@philipp-trommler.me>

## License

*yafg* has been published under a GPL 3.0 or later license. See the `LICENSE`
file for more information.

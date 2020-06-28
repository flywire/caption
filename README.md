# caption - manages markdown captions

*caption* manages captions by applying style and auto-numbering to content. The
vision is to apply captions to any content. For now only figures are supported
but the next candidate is likely to be tables.

*caption* is a fork of [yafg](https://git.sr.ht/~ferruck/yafg) - yet another
figure generator plugin for Python's Markdown. It's written and tested with
Python 2.7 and Python 3.6 as well as Markdown 3.1.1, but aims at supporting as
many versions as possible. If you encounter any problems with *caption* please
raise an [issue](https://github.com/flywire/caption/issues), or perhaps you want
to contact me through the e-mail address on my profile to contribute.

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

*caption* can be installed via `pip3 install git+https://github.com/flywire/caption`

### Standard Usage

When parsing your input, you can add *caption* to Markdown as follows:

```python
import caption

# ...

outputString = markdown.markdown(inputString, extensions = [caption.captionExtension(stripTitle=False)])
```

### Pelican

Pelican users can add *caption* to their generator process by adding it to the
`MARKDOWN` variable in the `pelicanconf.py` as follows:

```python
MARKDOWN = {
    'extensions_configs': {
        'caption': {
            'stripTitle': 'False',
        },
    },
}
```

### Options

Currently supported options are listed below:

* `captionPrefix` (default: `"Figure"`):

    The text to show at the front of the caption. A final non-breaking space
    is inserted between the content of `captionPrefix` and the actual figure
    number.

* `capcaptionClass` (default: `""`):

    The CSS class to add to the generated `<capcaption />` element.

* `captionNumbering` (default: `False`):

    Adds a caption number like "Figure 1:" in front of the caption. It's
	wrapped in a `<span />` for easier styling.

* `captionNumberClass` (default: `""`):

    The CSS class to add to the `<span />` element generated for the figure
    number.

* `captionClass` (default: `""`):

    The CSS class to add to the generated `<caption />` element.

* `stripTitle` (default: `False`):

    Removes the original `title` attribute from the `<img />` element. Since its
    usage is discouraged anyways (see below), this may be an option worth
    considering.

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

## License

*caption* has been published under a GPL 3.0 or later license. See the `LICENSE`
file for more information.

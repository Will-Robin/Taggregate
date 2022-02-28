# Taggregate

A library to aid figure numbering across multiple files using a tagging syntax. Figures are referred to in text and in legends by tags which have the following form:

```
{#f:name:p}
```

`f` is an indicator of the 'type' of item it refers to. For example, it could be a scheme, a main text figure, a supplementary figure or a table. The idea is that each tag of type `f` will have its own numbering separate to other types.

`name` is a unique identifier for the figure. It must consist of letters and `-` characters.

`p`: is a tag for the part of the text in which the tag is placed (`t` in text, `f` in a figure).

These tags are accumulated by the software across several files, then stored in a tag file into the order in which they are found in the texts past to the scripts. The contents of this tag file can then be placed in the header .yaml of a markdown document. A Pandoc filter can then be used to convert the tags in the texts to figure numbers upon compilation.

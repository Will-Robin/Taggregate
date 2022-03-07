# Taggregate

Numbering figures is a pain. It can be hard to keep figure numbers up to date, particularly across multiple documents. This code plays a role in part of a system which allows for automatic numbering of figures across multiple documents (explanation in progress...).

This ~library~ bunch of functions aids figure numbering across multiple files using a tagging syntax. Figures are referred to in text and in legends by tags which have the following three-part form:

```
{#f:name:p}
```

`f` is an indicator of the 'type' of item it refers to. For example, it could be a scheme, a main text figure, a supplementary figure or a table. The idea is that each tag of type `f` will have its own numbering separate to other types.

`name` is a unique identifier for the figure. It must consist of letters and `-` characters.

`p`: is a tag for the part of the text in which the tag is placed (`t` in text, `f` in a figure). This part of the tag aids in deciding which instances of the tags to prioritise for the numbering scheme.

These tags are accumulated by the software across several files, then stored in a tag file into the order in which they are found in the texts past to the scripts. The contents of this tag file can then be placed in the header `.yaml` of a markdown document.

A Pandoc filter can then be used to convert the tags in the texts to figure numbers upon compilation (have a look at [moonuscript](https://github.com/Will-Robin/moonuscript)).

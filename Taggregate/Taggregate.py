import os
import re
import yaml
from pathlib import Path


def loadConfig(file):
    """
    Get various parameters stored in a yaml config file.

    Parameters
    ----------
    file: str

    Returns
    -------
    header_info: dict
    """

    text = textFromFile(file)
    header_info = yaml.load(text, Loader=yaml.FullLoader)

    return header_info


def textFromFile(fname):
    """
    Read text from a file.

    Parameters
    ----------
    fname: str

    Returns
    -------
    text: str
    """

    with open(fname, "r") as f:
        text = f.read()

    return text


def getTagsFromFile(fname):
    """
    Read a file as text and find the figure tags within it.

    Parameters
    ----------
    fname: str

    Returns
    -------
    hits: list
    """

    tag_patt = "{#[a-z]:[a-z0-9_-]*:\w}"
    header_regex = "^---\n([\s\S]+?)---"

    text = textFromFile(fname)

    # remove header yaml so it does not interfere in the ordering of tags
    text = re.sub(header_regex, "", text)
    hits = re.findall(tag_patt, text)

    return hits


def getTagRangesFromFile(fname):
    """
    Read a file as text and find the figure tags within it.

    Parameters
    ----------
    fname: str

    Returns
    -------
    ranges: list of lists
    """

    tag_patt = "{#[a-z]:[a-z0-9_-]*:\w}"
    tag_range_patt = f"{tag_patt}[ ]?-[ ]?[A-Z]?{tag_patt}"

    text = textFromFile(fname)

    hits = re.findall(tag_range_patt, text)

    ranges = []
    for h in hits:
        indiv_tags = re.findall(tag_patt, h)
        ranges.append([getTagName(tag) for tag in indiv_tags])

    return ranges


def getTagRangesFromFiles(files):
    """
    Get ranged tag mentions from a group of files.

    Parameters
    ----------
    files: list

    Returns
    -------
    ranges: list
    """

    ranges = []
    for f in files:
        rn = getTagRangesFromFile(f)
        ranges.extend(rn)

    return ranges


def getTagTextMentions(fname):
    """
    Get the mentions of figure tags
    outside image captions.

    Parameters
    ----------
    fname: str

    Returns
    -------
    hits: list
    """

    image_patt = r"(?s)!\[(.*?)\]\("
    text = textFromFile(fname)

    tag_patt = "{#[a-z]:[a-z0-9_-]*:\w}"
    header_regex = "^---\n([\s\S]+?)---"

    # remove header yaml so it does not interfere in the ordering of tags
    text = re.sub(header_regex, "", text)
    # remove image tags
    text = re.sub(image_patt, "", text)
    hits = re.findall(tag_patt, text)

    return hits


def getTagsTextMentionsFromFiles(files):
    """
    Get the mentions of figure tags outside figure captions ordered by
    appearance in the list of text files.

    Parameters
    ----------
    files: list

    Returns
    -------
    results: list
    """

    results = []
    for f in files:
        results.extend(getTagTextMentions(f))

    return results


def getTagsImages(fname):
    """
    Get figure tags from within markdown image fields.

    Parameters
    ----------
    fname: str

    Returns
    -------
    hits: list
    """

    image_patt = r"(?s)!\[(.*?)\]\("
    text = textFromFile(fname)

    # remove header yaml so it does not interfere in the ordering of tags
    hits = re.findall(image_patt, text)

    return hits


def imageFieldsFromFiles(files):
    """
    Get the contents of image captions in a list of files.

    Parameters
    ----------
    files: list

    Returns
    -------
    images: list
    """

    images = []
    for f in files:
        images.extend(getTagsImages(f))

    return images


def getTagsFromImageFields(image_fields):
    """
    Get the captions from all images tags in a file.

    Parameters
    ----------
    image_fields: list

    Returns
    -------
    all_hits: list
    """

    tag_patt = "{#[a-z]:[a-z0-9_-]*:\w}"
    all_hits = []
    for i in image_fields:
        hits = re.findall(tag_patt, i)
        all_hits.extend(hits)

    return all_hits


def getTagName(tag):
    """
    Get the name field of a tag:

    {#x:name_field:t}

    Parameters
    ----------
    tag: str

    Returns
    -------
    name: str
    """

    name_regex = r"#[a-z]:[a-z0-9_-]*"

    name = re.findall(name_regex, tag)[0]

    return name


def tagsFromFiles(file_list, figure_wise=False):
    """
    Get an ordered list of tags from the file list (tags will be ordered in
    order of appearance according to the list of files)

    Parameters
    ----------
    file_list: list

    figure_wise: bool
        whether to arrange figures according to their first appearance in a
        figure (True), or in a figure or text (False)

    Returns
    -------
    ordered_tags: list
    """

    all_hits = []
    for f in file_list:
        hits = getTagsFromFile(f)
        all_hits.extend(hits)

    # remove duplicates
    ordered_tags = []
    if figure_wise:
        part_of_text_patt = r":(\w)}"
        for a in all_hits:
            name = getTagName(a)
            matches = re.findall(part_of_text_patt, a)
            if name in ordered_tags:
                pass
            elif matches[0] == "f":
                ordered_tags.append(name)
            else:
                pass

    else:
        for a in all_hits:
            name = getTagName(a)
            if name in ordered_tags:
                pass
            else:
                ordered_tags.append(name)

    return ordered_tags


def resolveRanges(tags, ranges):
    """
    Use tag ranges found to correctly order the tag list.

    Parameters
    ----------
    tags: list

    ranges: list

    Returns
    -------
    tags: list
    """

    missing_elements = []
    for r in ranges:
        for t in tags:
            if t == r[0]:
                pass
            elif t == r[1]:
                pass
            elif r[0][:-2] in t:
                missing_elements.append(t)
                tags.remove(t)

    for c, r in enumerate(ranges):
        b = tags.index(r[0])
        e = tags.index(r[1])
        tags.insert(e, missing_elements[c])

    return tags


def getHeaderYAML(text):
    """
    Get the header YAML from text.

    Parameters
    ----------
    text: str

    Returns
    -------
    header_yaml: str
    """

    header_regex = "^---\n([\s\S]+?)---"

    header = re.findall(header_regex, text)
    # re.findall returns a list. The header should be the first element of this
    # list.
    header_yaml = header[0]

    return header_yaml


def getHeader(fname):
    """
    Read in a file and return the information in the header YAML as a
    dictionary.

    WARNING: yaml.load can execute arbitrary Python code, so only use this
    script on trusted documents.

    Parameters
    ----------
    fname: str

    Returns
    -------
    header_info: dict
    """

    text = textFromFile(fname)
    header_yaml = getHeaderYAML(text)
    # Conversion of YAML to dict
    header_info = yaml.load(header_yaml, Loader=yaml.FullLoader)

    return header_info


def writeTagFileText(tags, delimiter="\n"):
    """
    Write the text entries for a lit of tags.

    Parameters
    ----------
    tags: list

    delimiter: str

    Returns
    -------
    text: str
    """

    text = ""
    for t in tags:
        text += f"{t}{delimiter}"

    return text


def writeTagFile(tags, fname, delimiter="\n"):
    """
    Write a list of tags to a file.

    Parameters
    ----------
    tags: list

    fname: str

    delimiter: str
    """

    text = writeTagFileText(tags, delimiter=delimiter)

    with open(fname, "w") as f:
        f.write(text)


def readTagFile(fname):
    """
    Read a list of tags from a file.

    Parameters
    ----------
    fname: str

    Returns
    -------
    new_tags: list
    """

    additions = textFromFile(fname)

    new_tags = [x for x in additions.split("\n") if x != ""]

    return new_tags

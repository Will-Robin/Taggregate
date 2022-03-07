import re
import yaml


def text_from_file(fname):
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

def load_config(file):
    """
    Get various parameters stored in a yaml config file.

    Parameters
    ----------
    file: str

    Returns
    -------
    header_info: dict
    """

    text = text_from_file(file)
    header_info = yaml.load(text, Loader=yaml.FullLoader)

    return header_info


def get_tags_from_file(fname):
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

    text = text_from_file(fname)

    # remove header yaml so it does not interfere in the ordering of tags
    text = re.sub(header_regex, "", text)
    hits = re.findall(tag_patt, text)

    return hits


def get_tag_ranges_from_file(fname):
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

    text = text_from_file(fname)

    hits = re.findall(tag_range_patt, text)

    ranges = []
    for h in hits:
        indiv_tags = re.findall(tag_patt, h)
        ranges.append([get_tag_name(tag) for tag in indiv_tags])

    return ranges


def get_tag_ranges_from_files(files):
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
        rn = get_tag_ranges_from_file(f)
        ranges.extend(rn)

    return ranges


def get_tag_text_mentions(fname):
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
    text = text_from_file(fname)

    tag_patt = "{#[a-z]:[a-z0-9_-]*:\w}"
    header_regex = "^---\n([\s\S]+?)---"

    # remove header yaml so it does not interfere in the ordering of tags
    text = re.sub(header_regex, "", text)
    # remove image tags
    text = re.sub(image_patt, "", text)
    hits = re.findall(tag_patt, text)

    return hits


def get_tags_text_mentions_from_files(files):
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
        results.extend(get_tag_text_mentions(f))

    return results


def get_tags_images(fname):
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
    text = text_from_file(fname)

    # remove header yaml so it does not interfere in the ordering of tags
    hits = re.findall(image_patt, text)

    return hits


def image_fields_from_files(files):
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
        images.extend(get_tags_images(f))

    return images


def get_tags_from_image_fields(image_fields):
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


def get_tag_name(tag):
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


def tags_from_files(file_list, figure_wise=False):
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
        hits = get_tags_from_file(f)
        all_hits.extend(hits)

    # remove duplicates
    ordered_tags = []
    if figure_wise:
        part_of_text_patt = r":(\w)}"
        for a in all_hits:
            name = get_tag_name(a)
            matches = re.findall(part_of_text_patt, a)
            if name in ordered_tags:
                pass
            elif matches[0] == "f":
                ordered_tags.append(name)
            else:
                pass

    else:
        for a in all_hits:
            name = get_tag_name(a)
            if name in ordered_tags:
                pass
            else:
                ordered_tags.append(name)

    return ordered_tags


def resolve_ranges(tags, ranges):
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
        e = tags.index(r[1])
        tags.insert(e, missing_elements[c])

    return tags


def get_header_yaml(text):
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


def get_header(fname):
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

    text = text_from_file(fname)
    header_yaml = get_header_yaml(text)
    # Conversion of YAML to dict
    header_info = yaml.load(header_yaml, Loader=yaml.FullLoader)

    return header_info


def write_tag_file_text(tags, delimiter="\n"):
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


def write_tag_file(tags, fname, delimiter="\n"):
    """
    Write a list of tags to a file.

    Parameters
    ----------
    tags: list

    fname: str

    delimiter: str
    """

    text = write_tag_file_text(tags, delimiter=delimiter)

    with open(fname, "w") as f:
        f.write(text)


def read_tag_file(fname):
    """
    Read a list of tags from a file.

    Parameters
    ----------
    fname: str

    Returns
    -------
    new_tags: list
    """

    additions = text_from_file(fname)

    new_tags = [x for x in additions.split("\n") if x != ""]

    return new_tags

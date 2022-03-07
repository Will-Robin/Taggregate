"""
Get all of the figure tags in a list of files defined in the config.

The tags are arrange either ir order of appearance, or in order of when they
are first defined as figures (figure_wise kwarg = True).
"""

from Taggregate import *


def main(files, outfile):
    """
    Run the tag extraction process.

    Parameters
    ----------
    files: list

    outfile: str

    Returns
    -------
    None
    """

    # Load the figure tags supplied as ranges
    ranges = get_tag_ranges_from_files(files)
    # Load the individual tags to figures
    tags = tags_from_files(files, figure_wise=True)
    # Add in any missing tags within range references
    resolved_tags = resolve_ranges(tags, ranges)

    # Create a list of the tags for output.
    output_tags = []
    for r in resolved_tags:
        output_tags.append(f"{{{r}:m}}")

    # Write to file
    write_tag_file(output_tags, outfile)


if __name__ == "__main__":
    out = load_config("config.yml")
    main(out["source-files"], out["tag-file"])

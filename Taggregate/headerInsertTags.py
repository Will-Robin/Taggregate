"""
Loads source text files and a 'tag file' generated from them, then adds in the
contents of the 'tag file' into the yaml header of the source files. The
resulting texts are saved in new files.
"""

from pathlib import Path
from Taggregate import *

# Name for the yaml field in which the figure tags will be stored.
tag_field = "manuscript-figures"


# Loads the config file which specifies the input and output files
config = loadConfig("config.yml")

for f in config["source-files"]:

    file = Path(f)

    # Load in the text
    text = textFromFile(f)

    # Get the header yaml so it can be replaced.
    header_yaml = getHeaderYAML(text)

    # Get the header of the file as a dict
    header = getHeader(f)

    # Load tags from the tag file
    tags = readTagFile(config["tag-file"])

    # Insert the tags into the header dict
    header[tag_field] = tags

    # Create new yaml string from the modified header dict
    new_yaml = yaml.dump(header, width=float("inf"))

    # Replace the old yaml header with the new one.
    new_text = text.replace(header_yaml, new_yaml)

    # Output to a file
    dest = config["compiled-directory"]

    with open(f"{dest}/{file.name}", "w") as f:
        f.write(new_text)

import re


def slugify(value):
    """Remove characters that could interfere with our URLs, and replace
    spaces with underscores.

    """
    if not value:
        return value
    
    # we don't want /, # or ? in our URL
    value = value.replace('/', '').replace('#', '').replace('?', '')

    # replace whitespace with underscores
    return re.sub('[-\\s]+', '_', value)


def creole_slugify(value):
    """Convert the given string to a slug consistent with heading IDs used
    by our creole parser.

    >>> creole_slugify("Only 20%!")
    "only-20"

    """
    if not value:
        return value

    # Only keep alphanumeric and space characters.
    value = re.sub(r"[^a-zA-Z0-9 ]+", "", value)

    # replace whitespace with underscores
    value = re.sub('[-\s]+', '-', value)

    return value.lower()


def remove_links(creole):
    """Remove all links in a given piece of creole text.

    >>> remove_links("[[foo]] [[http://bar|baz]]")
    "foo baz"

    """
    named_link = re.compile(r"""\[\[    # opening [[
                                [^]|]+? # anything that isn't | or ]
                                \|      # the | separator
                                ([^]]+) # name of the link, anything that isn't ]
                                \]\]    # closing ]]
                                """, re.VERBOSE)

    simple_link = re.compile(r"""\[\[    # opening [[
                                 ([^]]+) # inside the link, anything that isn't ]
                                 /]/]    # closing ]]
                                 """, re.VERBOSE)

    creole = re.sub(named_link, r"\1", creole)
    return re.sub(simple_link, r"\1", creole)

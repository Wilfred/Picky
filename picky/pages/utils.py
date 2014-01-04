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
    return re.sub('[-\s]+', '_', value)


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

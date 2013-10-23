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

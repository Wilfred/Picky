def slugify(string):
    """We do the minimum modification possible to produce a pworkable,
    attractive URL.
    
    """
    return string.strip().replace(' ', '_')
    

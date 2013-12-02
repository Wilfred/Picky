from __future__ import division
from datetime import timedelta

from django import template
from django.utils.timezone import now


register = template.Library()


@register.filter
def relative_time(dt):
    """Return a string describing how long ago this datetime is. Uses the
    same strings as timeago.js so the relative time is correct on page
    load.

    """
    if not dt:
        return "never"
    
    timesince = now() - dt
    
    if timesince < timedelta(minutes=1):
        return "less than a minute ago"

    elif timesince < timedelta(minutes=2):
        return "about a minute ago"

    elif timesince < timedelta(hours=1):
        return "%d minutes ago" % (timesince.total_seconds() / 60)

    elif timesince < timedelta(hours=2):
        return "about an hour ago"

    elif timesince < timedelta(days=1):
        return "%d hours ago" % (timesince.total_seconds() / (60 * 60))

    elif timesince < timedelta(days=2):
        return "a day ago"

    elif timesince < timedelta(days=30):
        return "%d days ago" % (timesince.total_seconds() / (60 * 60 * 24))

    elif timesince < timedelta(days=60):
        return "about a month ago"

    elif timesince < timedelta(days=365):
        return "%d months ago" % (timesince.total_seconds() / (60 * 60 * 24 * 30))

    elif timesince < timedelta(days=365 * 2):
        return "about a year ago"

    return "%d years ago" % (timesince.total_seconds() / (60 * 60 * 24 * 365))


@register.filter
def absolute_time(dt):
    if not dt:
        return "never"

    return dt.strftime("%Y %B %d, %H:%M")

from __future__ import division
from datetime import timedelta

from django import template
from django.utils.timezone import now


register = template.Library()


@register.filter
def relative_time(dt):
    timesince = now() - dt
    
    if timesince < timedelta(minutes=1):
        return "moments ago"

    elif timesince < timedelta(minutes=2):
        return "1 minute ago"

    elif timesince < timedelta(hours=1):
        return "%d minutes ago" % (timesince.total_seconds() / 60)

    elif timesince < timedelta(hours=2):
        return "1 hour ago"

    elif timesince < timedelta(days=1):
        return "%d hours ago" % (timesince.total_seconds() / (60 * 60))

    elif timesince < timedelta(days=2):
        return "1 day ago"

    elif timesince < timedelta(days=15):
        return "%d days ago" % (timesince.total_seconds() / (60 * 60 * 24))

    elif timesince < timedelta(days=90):
        return "%d weeks ago" % (timesince.total_seconds() / (60 * 60 * 24 * 7))

    return "%d months ago" % (timesince.total_seconds() / (60 * 60 * 24 * 7 * 30))

# -*- coding: utf-8 -*-
from datetime import datetime


def _timestamp(dt):
    """Return a timestamp from a datetime object."""
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return str(delta.total_seconds())

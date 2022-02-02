#!/usr/bin/env python3


def merge(*dicts):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dicts:
        result.update(dictionary)
    return result

#!/usr/bin/env python3

def split(predicate, iterable):
    """Split iterable in two lists - Predicate False and Predicate True"""
    true_list = []
    false_list = []
    for x in iterable:
        if predicate(x):
            true_list.append(x)
        else:
            false_list.append(x)
    return [false_list, true_list]


def has_tag(task, tag):
    tags = task.get('tags', [])
    if len(tags) == 0:
        return False
    return tag in tags

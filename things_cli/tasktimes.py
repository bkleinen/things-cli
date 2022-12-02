#!/usr/bin/env python3
import re
from functools import reduce

EST_REGEX = '#(\d+)$'
ACT_REGEX = '=(\d+)$'

"""Add time estimates and actual time spent to tasks."""

def summary(cli,tasks):
    result = []
    if cli.estimated_time:
        result.append(f'total time estimated: {_nice_time(_estimated_total(tasks))}')
    if cli.actual_time:
        result.append(f'total time logged: {_nice_time(_logged_total(tasks))}')
    return "\n".join(result)

def _estimated_total(tasks):
    return sum(tasks,EST_REGEX)

def _logged_total(tasks):
    return sum(tasks,ACT_REGEX)

def sum(tasks,regex):
    all_tags = [task.get('tags',None) for task in tasks]
    all_tags_flat = [item for list in all_tags if list is not None for item in list]
    all_times = [_extract_minutes(t,regex) for t in all_tags_flat]
    sum = total_time = reduce((lambda x, y: x + y),all_times)

    return sum

def _extract_minutes(str,regex = EST_REGEX):
    match = re.search(regex,str)
    if match:
        return int(match[1])
    return 0

def _nice_time(minutes):
    return f'{minutes // 60} hours {minutes % 60} minutes'


def txt_dumps(cli,task):
    if not (cli.estimated_time or cli.actual_time):
        return None

    times = []
    if cli.estimated_time:
        times.append(_time_dump(task,EST_REGEX,"** no estimate **"))

    if cli.actual_time:
        times.append(_time_dump(task,ACT_REGEX,"no log"))

    return "/".join(times)

def _time_dump(task,regex,missing_test):
    tags_with_estimate = None
    txt = ""
    if 'tags' not in list(task):
        return missing_test

    tags_with_estimate = list(filter(lambda t: _is_time_tag(t,regex),task['tags']))
    if tags_with_estimate and len(tags_with_estimate) > 0:
        return ", ".join(tags_with_estimate)
    else:
        return missing_test

def _is_time_tag(str,regex = EST_REGEX):
    """ checks for regex match, thus if it's a time tag """
    match = re.search(regex,str)
    if match:
      return True
    else:
      return False

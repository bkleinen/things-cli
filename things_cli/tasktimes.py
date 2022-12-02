#!/usr/bin/env python3
import re

EST_KEY = 'estimated_time'
EST_REGEX = '#(\d+)$'
ACT_KEY = 'actual_time'
ACT_REGEX = '=(\d+)$'

"""Add time estimates and actual time spent to tasks."""
def txt_dumps(cli,task):
    if not (cli.estimated_time or cli.actual_time):
        return None

    txt = ""
    if cli.estimated_time:
        tags_with_estimate = None
        if 'tags' not in list(task):
            txt = txt + "** no estimate **"
        else:
            tags_with_estimate = list(filter(lambda t: _has_time(t,EST_REGEX),task['tags']))
        estimates = "** no estimate **"
        if tags_with_estimate and len(tags_with_estimate) > 0:
            estimates = ", ".join(tags_with_estimate)
        txt = txt + estimates
    if cli.actual_time:
        txt = txt + "here actual time"

    return txt



def txt_dump_time(task, time_key = EST_KEY, regex = EST_REGEX):
    if 'tags' not in list(task):
        return
    tags_with_time = list(filter(lambda t: has_time(t,regex),task['tags']))
    if (len(tags_with_time) < 1):
        return
    first_time = tags_with_time[0]
    minutes = extract_minutes(first_time)
    task[time_key] = minutes


def _has_time(str,regex = EST_REGEX):
    match = re.search(regex,str)
    if match:
      return True
    else:
      return False

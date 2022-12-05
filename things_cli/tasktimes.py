#!/usr/bin/env python3

"""Add time estimates and actual time spent to task lists."""

import re
import time
from functools import reduce

# regular expressions to identity the time tags
# and extract the time in minutes -
# could be made configurable if needed.
EST_REGEX = r'#(\d+)$'
ACT_REGEX = r'=(\d+)$'


def collected(cli, time_estimates):
    if not cli.estimated_time:
        return ""
    estimated_minutes = reduce((lambda x, y: x + y), time_estimates)
    return f'total time estimated: {_nice_time(estimated_minutes)}'



def summary(cli, tasks_including_canceled, time_estimates, project=False):
    """Return estimated and actual time summaries."""
    if len(tasks_including_canceled) == 0:
        return ""
    result = []
    tasks, canceled = _split_canceled(tasks_including_canceled)
    if cli.estimated_time:
        estimated_minutes = _estimated_total(tasks)
        time_estimates.append(estimated_minutes)
        result.append(f'time estimated: {_nice_time(estimated_minutes)}')
        time_canceled = _estimated_total(canceled)
        if time_canceled != 0:
            result.append(f'canceled: {_nice_time(time_canceled)}')
        if project:
            now = time.time()
            result.append(f'Time now: {time.ctime(now)}')
            result.append(f'Time finished: {time.ctime(now+60*estimated_minutes)}')
    if cli.actual_time:
        result.append(f'time logged: {_nice_time(_logged_total(tasks))}')
        logged_canceled = _logged_total(canceled)
        if logged_canceled != 0:
            result.append(f'canceled: {_nice_time(logged_canceled)}')
    result.append("")
    return "\n".join(result)


def _estimated_total(tasks):
    return _sum(tasks, EST_REGEX)


def _logged_total(tasks):
    return _sum(tasks, ACT_REGEX)


def _is_canceled(task):
    status = task.get('status', 'none')
    return status == 'canceled'


def _split_canceled(tasks_including_canceled):
    canceled = []
    tasks = []
    for task in tasks_including_canceled:
        if _is_canceled(task):
            canceled.append(task)
        else:
            tasks.append(task)
    return tasks, canceled


def _sum(tasks, regex):
    if len(tasks) == 0:
        return 0
    all_tags = [task.get('tags', None) for task in tasks]
    all_tags_flat = [item for list in all_tags if list is not None for item in list]
    all_times = [_extract_minutes(t, regex) for t in all_tags_flat]
    if len(all_times) == 0:
        return 0
    return reduce((lambda x, y: x + y), all_times)


def _extract_minutes(tag, regex=EST_REGEX):
    match = re.search(regex, tag)
    if match:
        return int(match[1])
    return 0


def _nice_time(minutes):
    return f'{minutes // 60} hours {minutes % 60} minutes'


def time_details(cli, task):
    """Return time tags in concise form for txt_dumps."""
    if not (cli.estimated_time or cli.actual_time):
        return None
    if 'type' not in list(task):
        return None
    times = []
    if cli.estimated_time:
        times.append(_time_dump(task, EST_REGEX, "**no estimate**"))

    if cli.actual_time:
        times.append(_time_dump(task, ACT_REGEX, "no log"))

    return "/".join(times)


def _time_dump(task, regex, missing_text):
    tags_with_estimate = None
    if 'tags' not in list(task):
        return missing_text

    tags_with_estimate = list(filter(lambda t: _is_time_tag(t, regex), task['tags']))
    if tags_with_estimate and len(tags_with_estimate) > 0:
        return ", ".join(tags_with_estimate)
    return missing_text


def _is_time_tag(tag, regex=EST_REGEX):
    """Check for regex match, thus for time tag."""
    match = re.search(regex, tag)
    return bool(match)


SYMBOLS = {'canceled': '\u2612 ',
           'completed': '\u2611 ',
           'incomplete' : '\u2610 ',
           'none': ''}


def status_symbol(task):
    """Map task status to an unicode symbol."""
    status = task.get("status", "none")
    return SYMBOLS.get(status, "?")

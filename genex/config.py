# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

ONELINE = ('--prefix=oneline '
           '--font --text '
           '--boxes_flow=1.0 --char_margin=100.0 --line_margin=0.0001')

CONFIG = '--char_margin=3.1 --boxes_flow=1.0 --line_margin=0.25 '

Todo = collections.namedtuple('Todo', 'resource pages config')


def todo(resource: str, pages: tuple = None, **kwargs):
    """\
    >>> todo('master116.pdf', pages=(1,2, 3), groupme=True)
    Todo(resource='master116.pdf', pages=(1, 2, 3), config={'groupme': True})
    >>> todo('master116.pdf', pages=None)
    Todo(resource='master116.pdf', pages=None, config=None)
    """
    result = Todo(resource, pages=pages, config=kwargs if kwargs else None)
    return result


def prepare_files(files, pages: tuple = (5, 6)) -> list:
    """\
    >>> prepare_files(['master116', ('mitpage', (1, 2, 3))])
    [Todo(resource='master116', pages=(5, 6),...Todo(resource='mitpage', pages=(1, 2, 3)...)]
    """
    result = []
    for item in files:
        if isinstance(item, Todo):
            result.append(item)
            continue
        if isinstance(item, str):
            result.append(todo(item, pages=pages))
            continue
        if isinstance(item, tuple):
            result.append(todo(item[0], item[1]))
            continue
    return result

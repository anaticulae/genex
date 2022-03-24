# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import utila

ONELINE = ('--prefix=oneline '
           '--font --text '
           '--boxes_flow=1.0 --char_margin=100.0 --line_margin=0.0001 ')

CONFIG = '--char_margin=3.1 --boxes_flow=1.0 --line_margin=0.25 '

Todo = collections.namedtuple('Todo', 'resource name pages config')


def todo(resource: str, name: str = None, pages: tuple = None, **kwargs):
    """\
    >>> todo('resource/master116.pdf', pages=(1,2, 3), groupme=True)
    Todo(resource='resource/master116.pdf', name='resource_master116', pages=(1, 2, 3), config={'groupme': True})
    >>> todo('resource/master116.pdf', pages=None)
    Todo(resource='resource/master116.pdf', name='resource_master116', pages=None, config=None)
    """
    config = kwargs if kwargs else None
    if name is None:
        name = simple(resource)
    result = Todo(resource, name=name, pages=pages, config=config)
    return result


def simple(path: str) -> str:
    """\
    >>> simple('repository/bachelor/bachelor090.pdf')
    'bachelor_bachelor090'
    """
    parent = utila.file_name(utila.path_parent(path))
    filename = utila.file_name(path)
    result = f'{parent}_{filename}'
    return result


def prepare_files(files, pages: tuple = (5, 6)) -> list:
    """\
    >>> prepare_files(['resource/master116.pdf', ('resource/mitpage', (1, 2, 3))])
    [Todo(resource='resource/master116.pdf',...pages=(5, 6),...Todo(...pages=(1, 2, 3), config=None)]
    """
    result = []
    for item in files:
        if ispowertodo(item):
            result.append(powertodo_convert(item))
            continue
        if isinstance(item, Todo):
            result.append(item)
            continue
        if isinstance(item, str):
            result.append(todo(item, pages=pages))
            continue
        if isinstance(item, tuple):
            result.append(todo(resource=item[0], pages=item[1]))
            continue
    return result


def ispowertodo(item) -> bool:
    if item.__class__.__module__ == 'power.config':
        return True
    if hasattr(item, 'name'):
        return False
    return hasattr(item, 'config')


def powertodo_convert(item) -> Todo:
    # power import is not required
    return todo(resource=item.resource, pages=item.pages, **item.config)

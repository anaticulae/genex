# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import utila


def select_pages(path: str, select) -> str:
    """\
    Support merging multiple selected pages.
    """
    try:
        select, always = select
    except TypeError:
        always = False
    assert isinstance(select, object.__class__), f'class not: {type(select)}'
    pages = select_section(path, select=select)
    if not pages:
        if always:
            return ':'
        utila.debug(f'could not find section, skip: {select} in {path}')
        return None
    pages = pages2str(pages)
    return pages


def select_section(path: str, select) -> tuple:
    assert isinstance(select, object.__class__), f'class not: {type(select)}'
    sections = serializeraw.load_sections(path)
    flat = []
    for level in sections:
        # TODO: REPLACE WITH NICE ITERATOR TO IMPROVE CODE STYLE
        flat.append(level)
        flat.extend(level[:])
    collected = []
    for item in flat:
        if item.__class__ == select:
            collected.append((item.start, item.end))
    return collected


def pages2str(pages: tuple) -> str:
    """Merges tuple or list of tuples to `cli` --pages format.

    >>> pages2str((5,5))
    '5'
    >>> pages2str((1,5))
    '1:5'
    >>> pages2str([(1,5), (9,9)])
    '1:5,9'
    """
    if isinstance(pages, list):
        collected = [pages2str(item) for item in pages]
        return ','.join(collected)
    if (pages[0]) == pages[1]:
        return str(pages[0])
    return ':'.join([str(item) for item in pages])

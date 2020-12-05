# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================


def paged(files, default=None) -> dict:
    """Select pages, if given `(source, pages)`, to extract. If no pages
    are given, use `default` one."""
    result = {}
    for item in files:
        page = default
        if isinstance(item, tuple):
            item, page = item
        result[item] = page
    return result

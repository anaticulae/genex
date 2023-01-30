# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import resinf
import utila

ONELINE = ('--prefix=oneline '
           '--font --text '
           '--boxes_flow=1.0 --char_margin=100.0 --line_margin=0.0001 ')

CONFIG = '--char_margin=3.1 --boxes_flow=1.0 --line_margin=0.25 '


def bypages(item: resinf.Todo) -> int:
    maxpage = utila.parse_ints(item.name)
    if not maxpage:
        return 256
    pagepattern = item.pages
    if isinstance(pagepattern, tuple):
        return len(pagepattern)
    maxpage: int = int(maxpage[-1])
    if pagepattern in {None, ':'}:
        return maxpage
    parsed = utila.parse_pages(
        pagepattern,
        pagecount=maxpage,
    )
    count = len(parsed)
    return count

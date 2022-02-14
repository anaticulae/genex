# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================


def shorten_path(path: str, maxlength: int = 100) -> str:
    """\
    >>> shorten_path('rawmaker -j=auto -i=C:/usr/python//master110.pdf -o=C:/tmp/.tmp//master_master110 --char_margin=5.0')
    'rawmaker -j=auto -i=ython//master110.pdf -o=mp//master_master110 --char_margin=5.0'
    """
    path = path.split()
    result = []
    for item in path:
        if item.startswith('-i='):
            item = '-i=' + item[-20:]
        elif item.startswith('-o='):
            item = '-o=' + item[-20:]
        result.append(item)
    raw = ' '.join(result)
    raw = raw[-maxlength:]
    return raw

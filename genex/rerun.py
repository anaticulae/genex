# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
>>> CONTENT = '''
... processing: docinfo
... completed: docinfo
... runtime: 49 sec
... ::12>> groupme --toc -j=auto -i=decider_ref/bachelor_bachelor037 -o=decider_ref/bachelor_bachelor037 --pages=3,4
... groupme
... use 8 processes
... processing: toc
... '''
>>> parse_steps(CONTENT)
[(12, 'groupme --toc -j=auto -i=decider_ref/bachelor_bachelor037 -o=decider_ref/bachelor_bachelor037 --pages=3,4')]
>>> parse_steps(CONTENT, start=15)
[]
"""

import utila

PATTERN = utila.compiles(r'\:\:(\d{2})>>(.+)')


def parse_steps(log: str, start=None):
    result = []
    log = utila.from_raw_or_path(log)
    for line in PATTERN.finditer(log):
        number, cmd = int(line[1]), line[2]
        if start is not None and number < start:
            continue
        result.append((number, cmd.strip()))
    return result

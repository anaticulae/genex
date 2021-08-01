# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import serializeraw
import utilatest

import genex


@utilatest.longrun
def test_extract_bachelor37_abbreviation_table(testdir):
    """Shrink abbreviation table extractor to abbreviation table section."""
    files = [
        power.BACHELOR037_PDF,
    ]
    genex.extract(
        files,
        destination=testdir.tmpdir,
        groupme=True,
        sections=True,
        base=power.REPOSITORY,
        pages='0:15',
    )
    bachelor37 = os.path.join(testdir.tmpdir, 'bachelor_bachelor037')
    path = os.path.join(bachelor37, 'groupme__abbreviation_abbreviation.yaml')
    assert os.path.exists(path)
    table = serializeraw.load_abbreviation_table(path)
    # extract only one table on page 1
    assert len(table) == 26

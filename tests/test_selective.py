# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import hoverpower
import pytest
import serializeraw
import utilotest

import genex
import tests


@pytest.mark.xfail(reason='missing tooling')
@utilotest.longrun
@tests.requires(hoverpower.BACHELOR037_PDF)
def test_extract_bachelor37_abbrev_table(td):
    """Shrink abbreviation table extractor to abbreviation table section."""
    files = [
        hoverpower.BACHELOR037_PDF,
    ]
    genex.extract(
        files,
        dest=td.tmpdir,
        footnote=True,
        groupme=True,
        headnote=True,
        pagenumber=True,
        reftable=True,
        sections=True,
        base=hoverpower.REPO,
        pages='0:15',
    )
    bachelor37 = td.tmpdir.join('bachelor_bachelor037')
    path = os.path.join(bachelor37, 'reftable__abbrev_abbrev.yaml')
    assert os.path.exists(path)
    table = serializeraw.load_abbreviation_table(path)
    # extract only one table on page 1
    assert len(table) >= 26  # VALIDATED 26

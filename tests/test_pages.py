# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw
import pytest
import utilo
import utilotest

import genex
import tests


@pytest.mark.xfail(reason='missing tooling')
@utilotest.longrun
@tests.requires(hoverpower.BACHELOR090_PDF)
def test_select_titlepage(td):
    files = [
        hoverpower.BACHELOR090_PDF,
    ]
    genex.extract(
        files,
        dest=td.tmpdir,
        detector=False,
        footnote=True,
        groupme=True,
        headnote=True,
        pagenumber=True,
        sections=True,
        base=hoverpower.REPO,
        pages='0:10',
    )
    generated = td.tmpdir.join('bachelor_bachelor090')
    utilo.exists_assert(generated)
    selected = genex.select_pages(generated, select=iamraw.TitlePageSection)
    assert selected == '1'

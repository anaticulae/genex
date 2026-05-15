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
import utilotest

import genex
import tests


@pytest.mark.xfail(reason='missing tooling')
@utilotest.longrun
@tests.requires(hoverpower.DOCU009_PDF)
@tests.requires(hoverpower.HOME018_PDF)
def test_nopage_extract(td):
    generated = td.tmpdir.join('generated')
    pdfs = [
        hoverpower.DOCU009_PDF,
        hoverpower.HOME018_PDF,
    ]
    genex.extract_removepages(
        resources=pdfs,
        dest=generated,
        pagenumber=True,
        headnote=True,
        footnote=True,
        groupme=True,
        worker=len(pdfs),
    )
    assert os.path.exists(generated), str(generated)


@pytest.mark.xfail(reason='missing tooling')
@utilotest.nightly
@tests.requires(hoverpower.DOCU009_PDF)
@tests.requires(hoverpower.DOCU007_PDF)
def test_nopage_full(td):
    generated = td.tmpdir.join('generated')
    pdfs = [
        hoverpower.DOCU009_PDF,
        hoverpower.DOCU007_PDF,
    ]
    genex.extract_removepages(
        resources=pdfs,
        dest=generated,
        full=True,
        worker=len(pdfs),
    )
    assert os.path.exists(generated), str(generated)

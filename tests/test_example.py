# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import hoverpower
import utilo
import utilotest

import genex
import genex.example


def test_example_common_root():
    pdfs = [
        hoverpower.DOCU009_PDF,
        hoverpower.BACHELOR111_PDF,
    ]
    expected = {
        'docu_docu009',
        'bachelor_bachelor111',
    }
    root = utilotest.simplify_testfile_names(pdfs)
    # the expected order is not important
    root = set(root)  # pylint:disable=R0204
    assert root == expected


@utilotest.longrun
def test_example_extract(td):
    generated = td.tmpdir.join('generated')
    pdfs = [
        hoverpower.DOCU009_PDF,
        hoverpower.BACHELOR111_PDF,
    ]
    genex.extract(
        pdfs,
        generated,
        pages='0:5',
        bibliography=True,
        cleanup=True,
        detector=True,
        doctextstyle=True,
        figureo=True,
        footnote=True,
        groupme=True,
        headlines=True,
        headnote=True,
        optimize=True,
        pagenumber=True,
        sections=True,
        spacestation=True,
        tablero=True,
    )
    assert os.path.exists(generated), str(generated)


@utilotest.longrun
def test_example_disable_abbrev_step(td):
    """Disable groupme --abbreviation if sections is disabled cause
    groupme --abbreviations requires section_result."""
    generated = td.tmpdir.join('generated')
    pdfs = [
        hoverpower.DOCU009_PDF,
    ]
    genex.extract(
        pdfs,
        generated,
        pages='0:5',
        footnote=True,
        groupme=True,
        headnote=True,
        pagenumber=True,
        sections=False,
        base=hoverpower.REPO,
    )
    assert os.path.exists(generated), str(generated)


@utilotest.longrun
def test_example_sections_ref(td):
    generated = td.tmpdir.join('generated')
    pdfs = [
        hoverpower.DOCU009_PDF,
    ]
    genex.extract(
        pdfs,
        generated,
        pages='0:5',
        footnote=True,
        groupme=True,
        headnote=True,
        pagenumber=True,
        sections_ref=False,
        sections=False,
        base=hoverpower.REPO,
    )
    assert os.path.exists(generated), str(generated)


@utilotest.longrun
def test_example_nothing(td):
    """Only rawmaker is runned."""
    generated = td.tmpdir.join('generated')
    pdfs = [
        hoverpower.DOCU009_PDF,
    ]
    genex.extract(
        pdfs,
        generated,
        pages='0:5',
        pdfinfo=False,
        oneline=None,
        base=hoverpower.REPO,
    )
    assert os.path.exists(generated), str(generated)


@utilotest.longrun
def test_example_nothing_and_cleanup(td):
    """Only rawmaker and cleanup is runned."""
    generated = td.tmpdir.join('generated')
    pdfs = [
        hoverpower.DOCU009_PDF,
    ]
    genex.extract(
        pdfs,
        generated,
        pages='0:5',
        pdfinfo=False,
        cleanup=True,
        oneline=None,
        base=hoverpower.REPO,
    )
    assert os.path.exists(generated), str(generated)


def test_example_order():
    generated = genex.example.generate(
        files=['source/test.pdf'],
        outpath='dest',
        rawmaker='rawmaker_normal',
        oneline='rawmaker_oneline',
        config=dict(
            caption=True,
            magic=True,
        ),
        pages='0:10',
    )
    todo: str = ' && '.join(generated[0][0])
    # ensure to run caption before magic
    magics = utilo.findindex(todo, 'magic')
    assert len(magics) == 2
    # assert magics[0] < todo.find('caption') < magics[1]
    assert todo.find('caption') < magics[1]

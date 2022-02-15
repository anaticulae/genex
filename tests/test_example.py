# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import utila
import utilatest

import genex
import genex.example


def test_example_common_root():
    pdfs = [
        power.DOCU009_PDF,
        power.BACHELOR111_PDF,
    ]
    expected = {
        'docu_docu009',
        'bachelor_bachelor111',
    }
    root = utilatest.simplify_testfile_names(pdfs)
    # the expected order is not important
    root = set(root)  # pylint:disable=R0204
    assert root == expected


@utilatest.longrun
def test_example_extract(testdir):
    generated = os.path.join(testdir.tmpdir, 'generated')
    pdfs = [
        power.DOCU009_PDF,
        power.BACHELOR111_PDF,
    ]
    genex.extract(
        pdfs,
        generated,
        pages='0:5',
        detector=True,
        doctextstyle=True,
        figureo=True,
        groupme=True,
        tablero=True,
        sections=True,
        rawmaker_cleanup=True,
        spacestation=True,
        optimize=True,
    )
    assert os.path.exists(generated), str(generated)


@utilatest.longrun
def test_example_disable_abbreviation_step(testdir):
    """Disable groupme --abbreviation if sections is disabled cause
    groupme --abbreviations requires section_result."""
    generated = os.path.join(testdir.tmpdir, 'generated')
    pdfs = [
        power.DOCU009_PDF,
    ]
    genex.extract(
        pdfs,
        generated,
        pages='0:5',
        groupme=True,
        sections=False,
        base=power.REPOSITORY,
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
    magics = utila.findindex(todo, 'magic')
    assert len(magics) == 2
    # assert magics[0] < todo.find('caption') < magics[1]
    assert todo.find('caption') < magics[1]

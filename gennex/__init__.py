#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os

from gennex.config import CONFIG
from gennex.config import ONELINE
from gennex.example import extract
from gennex.example import generate
from gennex.example import run_job
from gennex.example import todolist
from gennex.nopage import extract_removepages
from gennex.pages import select_pages
from gennex.rerun import parse_steps

__version__ = '0.40.0'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

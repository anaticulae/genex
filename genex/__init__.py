#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os

from genex.config import CONFIG
from genex.config import ONELINE
from genex.example import extract
from genex.example import generate
from genex.example import run_job
from genex.example import todolist
from genex.nopage import extract_removepages
from genex.pages import select_pages
from genex.rerun import parse_steps

__version__ = '0.40.0'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

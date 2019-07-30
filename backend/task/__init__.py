#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import glob
import logging
import os

import rootpath

rootpath.append()

from paths import TASK_DIR

logger = logging.getLogger('TaskManager')
logger.info("[SYSTEM] Auto-imported files:",
            [file.split("/")[-1].strip(".py").strip("./") for file in glob.glob(os.path.join(TASK_DIR, "./*.py"))])

__all__ = [file.split("/")[-1].strip(".py").strip("./") for file in glob.glob(os.path.join(TASK_DIR, "./*.py"))]

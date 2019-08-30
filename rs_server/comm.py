# encoding: utf-8
import sys

import dos as DOS
import elog as LOG
from dos import *

aw_Sleep = Sleep

def StepTag(text):
    """
    测试用例,测试步骤标记
    """
    LOG.logTitle(text)

def aw_AssertStatistResult(statist_result,*args,**kwargs):

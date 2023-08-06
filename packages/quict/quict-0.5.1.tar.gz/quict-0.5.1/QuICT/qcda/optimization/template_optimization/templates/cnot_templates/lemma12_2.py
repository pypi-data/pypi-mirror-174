#!/usr/bin/env python
# -*- coding:utf8 -*-
# @TIME    : 2020/12/12 6:57 下午
# @Author  : Han Yu
# @File    : lemma12_2.py

from QuICT.core import *
from QuICT.core.gate import *


def lemma12_2():
    circuit = Circuit(4)
    CX | circuit([0, 1])
    CX | circuit([0, 2])
    CX | circuit([0, 3])
    CX | circuit([0, 1])
    CX | circuit([2, 3])
    CX | circuit([0, 2])
    CX | circuit([2, 3])
    return circuit

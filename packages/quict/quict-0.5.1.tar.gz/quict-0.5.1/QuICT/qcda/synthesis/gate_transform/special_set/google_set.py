#!/usr/bin/env python
# -*- coding:utf8 -*-
# @TIME    : 2021/3/20 5:00 下午
# @Author  : Han Yu
# @File    : IBMQ_set.py

from .. import InstructionSet
from ..transform_rule import xyx_rule

from QuICT.core.gate import *

GoogleSet = InstructionSet(
    GateType.fsim,
    [GateType.sx, GateType.sy, GateType.sw, GateType.rx, GateType.ry]
)
GoogleSet.register_one_qubit_rule(xyx_rule)

#!/usr/bin/env python
# -*- coding:utf8 -*-
# @TIME    : 2021/4/3 4:41 下午
# @Author  : Han Yu
# @File    : ustc_set

from .. import InstructionSet
from ..transform_rule import xyx_rule

from QuICT.core.gate import *

USTCSet = InstructionSet(
    GateType.cx,
    [GateType.rx, GateType.ry, GateType.rz, GateType.h, GateType.x]
)
USTCSet.register_one_qubit_rule(xyx_rule)

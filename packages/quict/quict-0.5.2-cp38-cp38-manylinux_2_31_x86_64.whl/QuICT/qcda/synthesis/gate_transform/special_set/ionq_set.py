#!/usr/bin/env python
# -*- coding:utf8 -*-
# @TIME    : 2021/4/3 3:32 下午
# @Author  : Han Yu
# @File    : ionq_set

from .. import InstructionSet
from ..transform_rule import xyx_rule

from QuICT.core.gate import *

IonQSet = InstructionSet(
    GateType.rxx,
    [GateType.rx, GateType.ry, GateType.rz]
)
IonQSet.register_one_qubit_rule(xyx_rule)

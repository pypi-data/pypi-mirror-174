#!/usr/bin/env python
# -*- coding:utf8 -*-
# @TIME    : 2021/4/4 10:01 上午
# @Author  : Han Yu
# @File    : ibmq_set

from .. import InstructionSet
from ..transform_rule import ibmq_rule

from QuICT.core.gate import *

IBMQSet = InstructionSet(
    GateType.cx,
    [GateType.rz, GateType.sx, GateType.x]
)
IBMQSet.register_one_qubit_rule(ibmq_rule)

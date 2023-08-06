#****************************************************************************
# Copyright 2019-2022 Matthew Ballance and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#*
#* Declares back-end interface API and associated data types
#****************************************************************************
from enum import IntEnum, IntFlag
from typing import Callable, List


class BinOp(IntEnum):
    pass

class UnaryOp(IntEnum):
    pass

class CompoundSolver(object):

    def solve(self, rs : 'RandState', fields, constraints, flags):
        raise NotImplementedError("solve")

class DataType(object):
    def mkRootField(self,
        ctxt : 'ModelBuildContext',
        name : str,
        is_ref : bool) -> 'ModelField':
        raise NotImplementedError("mkRootField")

    def mkTypeField(self,
        ctxt : 'ModelBuildContext',
        type : 'TypeField') -> 'ModelField':
        raise NotImplementedError("mkTypeField")

class DataTypeEnum(DataType):
    def name(self) -> str:
        raise NotImplementedError("name")

    def isSigned(self) -> bool:
        raise NotImplementedError("isSigned")

    def addEnumerator(self, name, val : 'ModelVal') -> bool:
        raise NotImplementedError("addEnumerator")

    def getDomain(self) -> 'TypeExprRangelist':
        raise NotImplementedError("getDomain")

class DataTypeInt(DataType):
    pass

class DataTypeStruct(DataType):

    def name(self) -> str:
        raise NotImplementedError("name")

    def addField(self, f : 'TypeField'):
        raise NotImplementedError("addField")

    def getFields(self) -> List['TypeField']:
        raise NotImplementedError("getFields")

    def getField(self, idx : int) -> 'TypeField':
        raise NotImplementedError("getField")

    def addConstraint(self, c : 'TypeConstraint'):
        raise NotImplementedError("addConstraint")

    def getConstraints(self) -> List['TypeConstraint']:
        raise NotImplementedError("getConstraints")

    def setCreateHook(self, hook : Callable):
        raise NotImplementedError("setCreateHook")

class ModelFieldFlag(IntFlag):
    NoFlags  = 0
    DeclRand = (1 << 0)
    UsedRand = (1 << 1)
    Resolved = (1 << 2)
    VecSize  = (1 << 3)

class ModelField(object):

    def name(self) -> str:
        raise NotImplementedError("name")

    def getDataType(self) -> DataType:
        raise NotImplementedError("getDataType")
    
    def getParent(self) -> 'ModelField':
        raise NotImplementedError("getParent")

    def setParent(self, parent : 'ModelField'):
        raise NotImplementedError("setParent")

    def constraints(self) -> List['ModelConstraint']:
        raise NotImplementedError("constraints")
    
    def addConstraint(self, c : 'ModelConstraint'):
        raise NotImplementedError("addConstraint")

    def fields(self) -> List['ModelField']:
        raise NotImplementedError("fields")

    def addField(self, f : 'ModelField'):
        raise NotImplementedError("addField")

    def getField(self, idx : int) -> 'ModelField':
        raise NotImplementedError("getField")

    def val(self) -> 'ModelVal':
        raise NotImplementedError("val")

    def clearFlag(self, flags : 'ModelFieldFlag'):
        raise NotImplementedError("clearFlag")

    def setFlag(self, flags : 'ModelFieldFlag'):
        raise NotImplementedError("setFlag")

    def isFlagSet(self, flags : 'ModelFieldFlag') -> bool:
        raise NotImplementedError("isFlagSet")

    def setFieldData(self, data):
        raise NotImplementedError("setFieldData")

    def getFieldData(self) -> object:
        raise NotImplementedError("getFieldData")



class ModelVal(object):

    def bits(self) -> int:
        raise NotImplementedError("bits")

    def setBits(self, bits : int) ->int:
        raise NotImplementedError("setBits")

    def val_u(self) -> int:
        raise NotImplementedError("val_u")

    def val_i(self) -> int:
        raise NotImplementedError("val_i")

    def set_val_i(self, v : int, bits : int=-1):
        raise NotImplementedError("set_val_i")

    def set_val_u(self, v : int, bits : int=-1):
        raise NotImplementedError("set_val_u")

class TypeFieldAttr(IntEnum):
    pass

class ModelBuildContext(object):

    def ctxt(self) -> 'Context':
        raise NotImplementedError("ctxt")

class RandState(object):

    def seed(self) -> str:
        raise NotImplementedError("seed")

    def randint32(self, low, high):
        raise NotImplementedError("randint32")

    def randbits(self, v : ModelVal):
        raise NotImplementedError("randbits")

    def setState(self, other : 'RandState'):
        raise NotImplementedError("setState")

    def clone(self) -> 'RandState':
        raise NotImplementedError("clone")

    def next(self) -> 'RandState':
        raise NotImplementedError("next")

class SolveFlags(IntEnum):
    pass

class TypeFieldAttr(IntFlag):
    NoAttr = 0
    Rand = (1 << 0)

#********************************************************************
#* TypeExpr
#********************************************************************

class TypeExpr(object):
    pass

class TypeExprRange(TypeExpr):

    def isSingle(self) -> bool:
        raise NotImplementedError("isSingle")

    def lower(self) -> 'TypeExpr':
        raise NotImplementedError("lower")

    def upper(self) -> 'TypeExpr':
        raise NotImplementedError("upper")

#********************************************************************
#* TypeField
#********************************************************************

class TypeField(object):

    def getParent(self) -> 'TypeField':
        raise NotImplementedError("getParent")

    def setParent(self, p : 'TypeField'):
        raise NotImplementedError("setParent")

    def getIndex(self) -> int:
        raise NotImplementedError("getIndex")

    def setIndex(self, idx : int):
        raise NotImplementedError("setIndex")

    def getDataType(self) -> 'DataType':
        raise NotImplementedError("getDataType")

    def name(self) -> str:
        raise NotImplementedError("name")

    def mkModelField(self, ctxt : 'ModelBuildContext') -> 'ModelField':
        raise NotImplementedError("mkModelField")


class TypeFieldPhy(TypeField):

    def getInit(self) -> 'ModelVal':
        raise NotImplementedError('getInit')


class Context(object):

    def findDataTypeEnum(self, name) -> DataTypeEnum:
        raise NotImplementedError("findDataTypeEnum")

    def mkDataTypeEnum(self, name) -> DataTypeEnum:
        raise NotImplementedError("mkDataTypeEnum")

    def addDataTypeEnum(self, t : DataTypeEnum) -> bool:
        raise NotImplementedError("addDataTypeEnum")

    def findDataTypeInt(self, is_signed : bool, width : int) -> DataTypeInt:
        raise NotImplementedError("findDataTypeInt")

    def mkDataTypeInt(self, is_signed : bool, width : int) -> DataTypeInt:
        raise NotImplementedError("mkDataTypeInt")

    def addDataTypeInt(self, t : DataTypeInt) -> bool:
        raise NotImplementedError("addDataTypeInt")

    def findDataTypeStruct(self, name) -> DataTypeStruct:
        raise NotImplementedError("findDataTypeStruct")

    def mkDataTypeStruct(self, name) -> DataTypeStruct:
        raise NotImplementedError("mkDataTypeStruct")

    def addDataTypeStruct(self, t : DataTypeStruct) -> bool:
        raise NotImplementedError("addDataTypeStruct")

    def mkRandState(self, seed : str) -> RandState:
        raise NotImplementedError("mkRandState")

    def mkModelBuildContext(self, ctxt : 'Context') -> ModelBuildContext:
        raise NotImplementedError("mkModelBuildContext")

    def mkTypeConstraintBlock(self, name) -> 'TypeConstraintBlock':
        raise NotImplementedError("mkTypeConstraintBlock")

    def mkTypeConstraintExpr(self, e : 'TypeExpr') -> 'TypeConstraintExpr':
        raise NotImplementedError("mkTypeConstraintExpr")

    def mkTypeConstraintIfElse(self, c : 'TypeExpr', ct : 'TypeConstraint') -> 'TypeConstraintIfElse':
        raise NotImplementedError("mkTypeConstraintIfElse")

    def mkTypeConstraintImplies(self, c : 'TypeExpr', b : 'TypeConstraint') -> 'TypeConstraintImplies':
        raise NotImplementedError("mkTypeConstraintImplies")

    def mkTypeConstraintSoft(self, c : 'TypeConstraintExpr') -> 'TypeConstraintSoft':
        raise NotImplementedError("mkTypeConstraintSoft")

    def mkTypeConstraintUnique(self, e : List['TypeExpr']) -> 'TypeConstraintUnique':
        raise NotImplementedError("mkTypeConstraintUnique")

    def mkTypeExprBin(self, lhs : 'TypeExpr', op : BinOp, rhs : 'TypeExpr') -> 'TypeExprBin':
        raise NotImplementedError("mkTypeExprBin")

    def mkTypeFieldPhy(self,
        name,
        dtype : 'DataType',
        own_dtype : bool,
        attr,
        init : 'ModelVal') -> 'TypeFieldPhy':
        raise NotImplementedError("mkTypeFieldPhy")

    def mkTypeFieldRef(self,
        name,
        dtype : 'DataType',
        attr) -> 'TypeFieldRef':
        raise NotImplementedError("mkTypeFieldRef")


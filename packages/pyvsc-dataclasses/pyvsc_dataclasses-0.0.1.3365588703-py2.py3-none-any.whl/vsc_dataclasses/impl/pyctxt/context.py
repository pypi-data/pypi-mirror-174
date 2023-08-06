
import vsc_dataclasses.impl as impl
from vsc_dataclasses.impl.pyctxt.type_field_phy import TypeFieldPhy
from .data_type_struct import DataTypeStruct
from .data_type_enum import DataTypeEnum
from .data_type_int import DataTypeInt
from .model_build_context import ModelBuildContext
from .rand_state import RandState


class Context(impl.Context):
    """Pure-python stub implementation of context"""

    def __init__(self):
        self._dt_struct_m = {}
        self._dt_enum_m = {}
        self._dt_sint_m = {}
        self._dt_uint_m = {}

    def findDataTypeEnum(self, name) -> DataTypeEnum:
        if name in self._dt_enum_m.keys():
            return self._dt_enum_m[name]
        else:
            return None

    def mkDataTypeEnum(self, name) -> DataTypeEnum:
        return DataTypeEnum(name, True)

    def addDataTypeEnum(self, t : DataTypeEnum) -> bool:
        if t._name not in self._dt_enum_m.keys():
            self._dt_enum_m[t._name] = t
        else:
            return False
        return True

    def findDataTypeInt(self, is_signed : bool, width : int) -> DataTypeInt:
        ret = None
        if is_signed:
            if width in self._dt_sint_m.keys():
                ret = self._dt_sint_m[width]
        else:
            if width in self._dt_uint_m.keys():
                ret = self._dt_uint_m[width]
        return ret

    def mkDataTypeInt(self, is_signed : bool, width : int) -> DataTypeInt:
        return DataTypeInt(is_signed, width)

    def addDataTypeInt(self, t : DataTypeInt) -> bool:
        if t._is_signed:
            if t._width in self._dt_sint_m.keys():
                return False
            else:
                self._dt_sint_m[t._width] = t
        else:
            if t._width in self._dt_uint_m.keys():
                return False
            else:
                self._dt_uint_m[t._width] = t
        return True

    def findDataTypeStruct(self, name) -> DataTypeStruct:
        if name in self._dt_struct_m.keys():
            return self._dt_struct_m[name]
        else:
            return None

    def mkDataTypeStruct(self, name) -> DataTypeStruct:
        return DataTypeStruct(name)

    def addDataTypeStruct(self, t : DataTypeStruct) -> bool:
        if t.name() not in self._dt_struct_m.keys():
            self._dt_struct_m[t.name()] = t
            return True
        else:
            return False

    def mkModelBuildContext(self, ctxt : 'Context') -> ModelBuildContext:
        return ModelBuildContext(ctxt)

    def mkRandState(self, seed : str) -> RandState:
        return RandState(seed)

    def mkTypeFieldPhy(self,
        name,
        dtype : 'DataType',
        own_dtype : bool,
        attr,
        init : 'ModelVal') -> 'TypeFieldPhy':
        return TypeFieldPhy(name, dtype, init)

    def mkTypeFieldRef(self,
        name,
        dtype : 'DataType',
        attr) -> 'TypeFieldRef':
        raise NotImplementedError("mkTypeFieldRef")

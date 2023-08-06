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
#****************************************************************************

from .field_scalar_impl import FieldScalarImpl
from .modelinfo import ModelInfo
from .typeinfo_vsc import TypeInfoVsc


class TypeInfoScalar(TypeInfoVsc):

    def __init__(self, is_signed):
        super().__init__(None, None)
        self.is_signed = is_signed

    def createInst(
            self,
            modelinfo_p : ModelInfo,
           name, 
           idx):
        field = FieldScalarImpl(name, self, idx)

        # Get the appropriate type/inst object
        field._modelinfo.libobj = modelinfo_p.libobj.getField(idx)

        modelinfo_p.addSubfield(field._modelinfo)
        return field

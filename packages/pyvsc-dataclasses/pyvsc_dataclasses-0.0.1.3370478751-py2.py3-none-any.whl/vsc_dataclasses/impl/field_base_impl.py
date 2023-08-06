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
#
# Created on May 25, 2022
#
# @author: mballance
#****************************************************************************

from .context import Context

from .ctor import Ctor
from .expr import Expr
from .modelinfo import ModelInfo


class FieldBaseImpl(object):
    
    def __init__(self, name, typeinfo, idx):
        self._modelinfo = ModelInfo(self, name, typeinfo, idx)
        
    def _to_expr(self):
        ctor = Ctor.inst()

        if ctor.is_type_mode():
            print("FieldScalarImpl._to_expr (%s)" % self._modelinfo.name, flush=True)
            ref = ctor.ctxt().mkTypeExprFieldRef()
            mi = self._modelinfo
            while mi._parent is not None:
                print("  IDX: %d" % mi._idx)
                ref.addIdxRef(mi._idx)
                print("MI: %s" % str(mi))
                mi = mi._parent

            print("is_topdown_scope: %d" % mi._is_topdown_scope)
            if mi._is_topdown_scope:            
                ref.addRootRef()
            else:
                ref.addActiveScopeRef(-1)
        else:        
            print("FieldScalarImpl._to_expr (%s)" % self.model().name(), flush=True)
            ref = ctor.ctxt().mkModelExprFieldRef(self.model())
        
        return Expr(ref)
    

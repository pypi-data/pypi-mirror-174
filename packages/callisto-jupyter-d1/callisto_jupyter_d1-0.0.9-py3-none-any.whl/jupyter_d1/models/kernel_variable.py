from typing import List, Optional

from pydantic import BaseModel

from .base_wrapper import BaseWrapper
from .JSONType import JSONType


class KernelVariable(BaseModel):
    name: str
    type: Optional[str]
    abbreviated: Optional[bool] = False
    has_next_page: Optional[bool] = False
    value: Optional[JSONType]
    summary: Optional[str]


class KernelVariableWrapper(BaseWrapper):
    single_var: KernelVariable


class KernelVariablesWrapper(BaseWrapper):
    vars: List[KernelVariable]

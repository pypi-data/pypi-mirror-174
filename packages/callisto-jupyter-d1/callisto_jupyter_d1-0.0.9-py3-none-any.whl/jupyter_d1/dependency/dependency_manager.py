from abc import ABC, abstractmethod
from typing import Any, Dict, List
from uuid import UUID

from ..utils import Connection


class DependencyManager(ABC):
    def __init__(self, kernel_name: str, kernelspec: Dict[str, Any]):
        self.kernel_name = kernel_name
        self.kernelspec = kernelspec

    @abstractmethod
    async def connect(self, connection: Connection) -> None:
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self, connection: Connection) -> None:
        raise NotImplementedError

    @abstractmethod
    async def execute(
        self, request_id: UUID, command: str, subcommand: str, args: List[str]
    ) -> str:
        raise NotImplementedError

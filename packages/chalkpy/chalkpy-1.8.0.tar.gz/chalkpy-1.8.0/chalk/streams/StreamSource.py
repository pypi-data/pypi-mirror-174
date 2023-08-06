import typing
from typing import Optional, TypeVar

from pydantic import BaseModel
from typing_extensions import Protocol

T = TypeVar("T")


class StreamSource(Protocol[T]):
    Message: typing.Any
    consumer_config: Optional[BaseModel]

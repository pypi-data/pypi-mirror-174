from collections.abc import Awaitable
from typing import Generic, TypeVar

from selva.di import service

from .context import RequestContext

__all__ = ("FromRequest",)

T = TypeVar("T")


class FromRequest(Generic[T]):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        service(provides=cls.__orig_bases__[0])(cls)

    def from_request(self, context: RequestContext) -> T | Awaitable[T]:
        raise NotImplementedError()

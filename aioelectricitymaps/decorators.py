"""Decorators for aioelectricitymaps."""
from __future__ import annotations

from collections.abc import Callable, Coroutine
from typing import Any, ParamSpec, TypeVar

from .exceptions import SwitchedToLegacyAPI

_R = TypeVar("_R")
_P = ParamSpec("_P")


def retry_legacy(
    func: Callable[_P, Coroutine[Any, Any, _R]],
) -> Callable[_P, Coroutine[Any, Any, _R]]:
    """Decorator to retry a function with the legacy API if SwitchedToLegacyAPI is raised."""

    async def inner(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        try:
            result = await func(*args, **kwargs)
        except SwitchedToLegacyAPI:
            result = await func(*args, **kwargs)

        return result

    return inner

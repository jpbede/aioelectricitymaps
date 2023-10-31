"""Decorators for aioelectricitymaps."""

from .exceptions import SwitchedToLegacyAPI


def retry_legacy(func):
    """Decorator to retry a function with the legacy API if SwitchedToLegacyAPI is raised."""

    async def inner(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
        except SwitchedToLegacyAPI:
            result = await func(*args, **kwargs)

        return result

    return inner

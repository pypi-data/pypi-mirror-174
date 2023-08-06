from .__about__ import (  # noqa
    __author__,
    __copyright__,
    __email__,
    __license__,
    __summary__,
    __title__,
    __uri__,
    __version__,
)
from .application import Application
from .clients import client
from .templates import template_global
from .wrappers import endpoint, require_http_same_origin

__all__ = [
    "__author__",
    "__copyright__",
    "__email__",
    "__license__",
    "__summary__",
    "__title__",
    "__uri__",
    "__version__",
    "Application",
    "client",
    "template_global",
    "endpoint",
    "require_http_same_origin",
]

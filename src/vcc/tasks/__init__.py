"""
VCC Task Framework.

Task classes encapsulate reusable units of work that can be executed
from the command line, scheduled jobs or the web interface.
"""

from .base import BaseTask

__all__ = ["BaseTask"]
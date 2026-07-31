"""
VCC - Base Task

Provides the common infrastructure for executable tasks.

A task is a reusable unit of work that can be executed from:

- run.py
- the web interface
- scheduled jobs
- future automation

Business logic belongs in subclasses.
This base class only provides shared infrastructure.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from time import perf_counter

from src.vcc.database import Database
from src.vcc.logger import get_logger
from src.vcc.repository import Repository


class BaseTask(ABC):
    """
    Base class for all executable VCC tasks.
    """

    def __init__(self) -> None:

        self.logger = get_logger()

        self.database = Database()
        self.database.initialize()

        self.repository = Repository(self.database)

    @property
    def name(self) -> str:
        """
        Human-readable task name.
        """

        return self.__class__.__name__

    @abstractmethod
    def run(self):
        """
        Execute the task.
        """

    def execute(self):
        """
        Execute the task while automatically handling:

        - logging
        - timing
        - database cleanup
        """

        start = perf_counter()

        self.logger.info("")
        self.logger.info("%s", self.name)
        self.logger.info("-----------------------------------")

        try:

            return self.run()

        finally:

            elapsed = perf_counter() - start

            self.database.close()

            self.logger.info("")
            self.logger.info(
                "%s completed in %.2f seconds",
                self.name,
                elapsed,
            )
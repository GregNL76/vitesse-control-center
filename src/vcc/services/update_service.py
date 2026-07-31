from __future__ import annotations

from src.vcc.auditor.update_auditor import UpdateAuditor
from src.vcc.mappers import (
    DuplicateUpdateMapper,
    OrphanUpdateMapper,
)
from src.vcc.repository import Repository


class UpdateService:

    def __init__(self, repository: Repository):

        self.repository = repository

        self.orphan_mapper = OrphanUpdateMapper()
        self.duplicate_mapper = DuplicateUpdateMapper()

    def missing_updates(self):

        return UpdateAuditor(self.repository).audit()

    def orphan_updates(self):

        rows = self.repository.orphan_updates()

        return self.orphan_mapper.map(rows)

    def duplicate_updates(self):

        rows = self.repository.duplicate_update_files()

        return self.duplicate_mapper.map(rows)
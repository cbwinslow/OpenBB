"""Research report service."""

import logging
from datetime import datetime
from typing import Dict
from uuid import uuid4

from openbb_core.app.model.abstract.singleton import SingletonMeta
from openbb_core.app.model.research import ResearchReport, ResearchRequest, ResearchSection

logger = logging.getLogger("uvicorn.error")


class ResearchService(metaclass=SingletonMeta):
    """Service orchestrating research report generation."""

    def __init__(self) -> None:
        import sqlite3
        self._db_connection = sqlite3.connect("research_reports.db")
        self._db_cursor = self._db_connection.cursor()
        self._db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS research_reports (
                id TEXT PRIMARY KEY,
                topic TEXT,
                created_at TEXT,
                sections TEXT
            )
        """)
        self._db_connection.commit()
    async def create_report(self, request: ResearchRequest) -> ResearchReport:
        """Create a research report placeholder."""
        section = ResearchSection(
            title="Summary",
            content=f"Automated summary for {request.topic}",
        )
        report = ResearchReport(
            id=str(uuid4()),
            topic=request.topic,
            created_at=datetime.utcnow(),
            sections=[section],
        )
        self._reports[report.id] = report
        logger.info("Created research report %s", report.id)
        return report

    async def get_report(self, report_id: str) -> ResearchReport | None:
        """Retrieve a stored research report."""
        return self._reports.get(report_id)

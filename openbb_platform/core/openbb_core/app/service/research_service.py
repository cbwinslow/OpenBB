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

    async def create_report(self, request: ResearchRequest) -> ResearchReport:
        """
        Generate a new research report with a unique ID and a default summary section based on the provided request topic.
        
        Parameters:
            request (ResearchRequest): The research request containing the topic for the report.
        
        Returns:
            ResearchReport: The newly created research report instance.
        """
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
        """
        Retrieve a research report by its unique ID.
        
        Parameters:
            report_id (str): The unique identifier of the research report.
        
        Returns:
            ResearchReport | None: The corresponding research report if found, otherwise None.
        """
        return self._reports.get(report_id)

"""Models for research report generation."""

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    """Request model for creating a research report."""

    topic: str = Field(..., description="Topic to research")


class ResearchSection(BaseModel):
    """Section of a research report."""

    title: str
    content: str


class ResearchReport(BaseModel):
    """Research report model."""

    id: str
    topic: str
    created_at: datetime
    sections: List[ResearchSection]

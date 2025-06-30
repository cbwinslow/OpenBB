"""Research report router."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from openbb_core.app.model.research import ResearchReport, ResearchRequest
from openbb_core.app.service.research_service import ResearchService

router = APIRouter(prefix="/research", tags=["Research"])


async def get_service() -> ResearchService:
    """Dependency to get research service."""
    return ResearchService()


@router.post("/", response_model=ResearchReport)
async def create_research(
    request: ResearchRequest,
    service: Annotated[ResearchService, Depends(get_service)],
) -> ResearchReport:
    """Create a research report using the multi-agent workflow."""
    return await service.create_report(request)


@router.get("/{report_id}", response_model=ResearchReport)
async def get_research(
    report_id: str,
    service: Annotated[ResearchService, Depends(get_service)],
) -> ResearchReport:
    """Retrieve a research report by id."""
    report = await service.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

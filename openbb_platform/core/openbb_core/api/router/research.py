"""Research report router."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from openbb_core.app.model.research import ResearchReport, ResearchRequest
from openbb_core.app.service.research_service import ResearchService

router = APIRouter(prefix="/research", tags=["Research"])


async def get_service() -> ResearchService:
    """
    Provides an instance of the ResearchService for dependency injection in FastAPI endpoints.
    
    Returns:
        ResearchService: An instance of the research service.
    """
    return ResearchService()


@router.post("/", response_model=ResearchReport)
async def create_research(
    request: ResearchRequest,
    service: Annotated[ResearchService, Depends(get_service)],
) -> ResearchReport:
    """
    Create a new research report based on the provided request data.
    
    Parameters:
        request (ResearchRequest): The data required to generate the research report.
    
    Returns:
        ResearchReport: The generated research report.
    """
    return await service.create_report(request)


@router.get("/{report_id}", response_model=ResearchReport)
async def get_research(
    report_id: str,
    service: Annotated[ResearchService, Depends(get_service)],
) -> ResearchReport:
    """
    Retrieve a research report by its unique identifier.
    
    Raises an HTTP 404 exception if the report does not exist.
    
    Parameters:
        report_id (str): The unique identifier of the research report to retrieve.
    
    Returns:
        ResearchReport: The research report corresponding to the given ID.
    """
    report = await service.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

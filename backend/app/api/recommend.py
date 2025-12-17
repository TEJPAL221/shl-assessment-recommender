from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from backend.app.retrieval.semantic_search import SemanticSearchEngine

router = APIRouter()
engine = SemanticSearchEngine()


class RecommendRequest(BaseModel):
    query: str


class AssessmentResponse(BaseModel):
    assessment_name: str
    assessment_url: str
    description: str
    test_type: List[str]
    duration: str
    remote_testing: str
    adaptive_support: str


@router.post("/recommend", response_model=List[AssessmentResponse])
def recommend(req: RecommendRequest):
    return engine.search(req.query, top_k=10)

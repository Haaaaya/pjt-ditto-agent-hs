from pydantic import BaseModel, Field


class Wordscores(BaseModel):
    scores: dict[str, float] = Field(..., description="各単語のスコア")

class ScoreResult(BaseModel):
    score: float
    success: str


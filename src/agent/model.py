from pydantic import BaseModel, Field
from typing import Dict

class Wordscores(BaseModel):
    scores: Dict[str, float] = Field(..., description="各単語のスコア")

    @property
    def text(self) -> str:
        return f"単語スコア: {self.scores}"

class ScoreResult(BaseModel):
    score: float = Field(..., description="全体スコア")
    success: str = Field(..., description="")

    @property
    def text(self) -> str:
        return f"総合評価: スコア={self.score:.2f}, 判定={self.success}"

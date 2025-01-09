from pydantic import BaseModel, Field
from typing import Dict

class Wordscore(BaseModel):
    word : str = Field(..., description="単語")
    score: int = Field(..., ge=-20, le = 100, description="単語のスコア")

class ScoreResult(BaseModel):
    score: float = Field(..., description="全体スコア")
    success: str = Field(..., description="")

    @property
    def text(self) -> str:
        return f"総合評価: スコア={self.score:.2f}, 判定={self.success}"

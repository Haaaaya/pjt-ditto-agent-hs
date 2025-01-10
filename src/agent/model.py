from pydantic import BaseModel, Field
from typing import List


class Wordscore(BaseModel):
    word: str = Field(..., description="単語")
    score: int = Field(..., ge=-20, le=100, description="単語のスコア")


class ScoreResult(BaseModel):
    score: float = Field(..., description="全体スコア")
    success: str = Field(..., description="")

    @property
    def text(self) -> str:
        return f"総合評価: スコア={self.score:.2f}, 判定={self.success}"


####################################################################################


class Appearance(BaseModel):
    height: str = Field(..., description="身長")
    hair: str = Field(..., description="髪型と色")
    style: str = Field(..., description="ファッションスタイル")


class Personality(BaseModel):
    strengths: str = Field(..., description="性格の長所")
    weaknesses: str = Field(..., description="性格の短所")
    values: str = Field(..., description="大切にしている価値観")


class RomanticPreferences(BaseModel):
    view: str = Field(..., description="恋愛観")
    experience: str = Field(..., description="恋愛経験")
    idealType: str = Field(..., description="理想のタイプ")
    preferredDate: str = Field(..., description="好みのデート")


class DailyLife(BaseModel):
    partTimeJob: str = Field(..., description="アルバイトの内容")
    friendships: str = Field(..., description="友人関係")
    weekends: str = Field(..., description="週末の過ごし方")


class FutureGoals(BaseModel):
    career: str = Field(..., description="将来のキャリア目標")
    lifestyle: str = Field(..., description="目指すライフスタイル")


class Persona(BaseModel):
    name: str = Field(..., description="名前")
    age: int = Field(..., description="年齢")
    gender: str = Field(..., description="性別")
    occupation: str = Field(..., description="職業")
    location: str = Field(..., description="居住地")
    appearance: Appearance = Field(..., description="外見")
    personality: Personality = Field(..., description="性格")
    romanticPreferences: RomanticPreferences = Field(..., description="恋愛の好み")
    hobbies: List[str] = Field(..., description="趣味")
    dailyLife: DailyLife = Field(..., description="日常生活")
    futureGoals: FutureGoals = Field(..., description="将来の目標")
    likes: List[str] = Field(..., description="好きなもの")
    dislikes: List[str] = Field(..., description="嫌いなもの")
    skills: str = Field(..., description="スキル")


############################################################################################

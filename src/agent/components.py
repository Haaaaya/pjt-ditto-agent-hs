from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from model import (Wordscores, ScoreResult)
from typing import Dict
import json

class ChatVectorizer:
    def __init__(self, model: ChatVertexAI):
        self.model = model
        
    def run(self, text: str) -> Wordscores:
        prompt = ChatPromptTemplate([
            (
                "system",
                "あなたは、テキストから特徴的な単語をいくつか抽出し、単語がポジティブであるかネガティブであるかを判断する専門家です。"
            ), (
                "human",
                "抽出した各単語には -1（非常にネガティブ）から 1（非常にポジティブ）までのスコアを細かく割り当ててください。"
                "テキスト：{text}"
            ),
        ])
        chain = prompt | self.model.with_structured_output(Wordscores)
        result = chain.invoke({"text": text}) # type: ignore
        print(f"this is res{result}")
        return Wordscores(scores = result)

class ChatScorer:
    def calculate_score(self, word_scores: Dict[str,float]) -> ScoreResult:
        score = sum(word_scores.values()) / len(word_scores) if word_scores else 0.0
        success = "成功" if score > 0.5 else "失敗"
        return ScoreResult(score=score, success=success)

class ResponseCreator:
    def __init__(self, model: ChatVertexAI):
        self.model = model

    def run(self, score: float, base_response: str) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "あなたは告白の結果とスコアに応じて告白の返事を作成する専門家です。スコアが1に近いほど好意的であり、スコアが-1に近いほど好意的でないことを示します。"),
            ("human", "告白の結果：{base_response} 、スコア：{score}の場合について、自然な返事を1つ作成してください。")
        ])
        
        chain = prompt | self.model
        result = chain.invoke({"base_response":base_response, "score": score})
        return str(result.content)

if __name__ == "__main__":
    model = ChatVertexAI(model_name="gemini-1.5-flash-002", temperature=0.0)
    vectorizer = ChatVectorizer(model=model)
    scorer = ChatScorer()
    response_creator = ResponseCreator(model=model)
    
    sample_texts = [
        "ずっと伝えたかったんだけど、あなたのことがとても好きです。もしよければ、これからもっと一緒に過ごしたいな。",
        "正直、もうこれ以上待てない気がする。ずっと好きだったけど、今まで何も言えなかった自分が情けなくて。"
    ]
    
    for text in sample_texts:
        print(f"入力: {text}")
        
        scores = vectorizer.run(text)
        print(f"単語スコア: {scores}")
        
        # scores = scorer.calculate_score(scores.scores)
        # print(f"総合スコア: {scores.score:.2f}")
        
        # response = response_creator.run(scores.score,scores.success)
        # print(f"応答: {response}")
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from model import Wordscores, ScoreResult
from typing import Dict
import json

class ChatVectorizer:
    def __init__(self, model: ChatVertexAI):
        self.model = model
        
    def run(self, text: str) -> Wordscores:
        prompt = ChatPromptTemplate([
            (
                "system",
                "テキストから感情を表す単語を抽出し、ポジティブ/ネガティブの度合いを数値化してください。スコアは-1から1の範囲で設定してください。"
            ),
            (
                "human",
                "抽出した単語とそのスコアを辞書形式として出力してください。"
                "コードブロックは使用しないでください"
                "以下のテキストを分析してください：{input_text}"
            )
        ])
        
        chain = prompt | self.model | StrOutputParser()
        response = chain.invoke({"input_text": text})
        result  = json.loads(response)
        return Wordscores(scores = result)

class ChatScorer:
    def calculate_score(self, word_scores: Dict[str, float]) -> ScoreResult:
        score = sum(word_scores.values()) / len(word_scores) if word_scores else 0.0
        success = "成功" if score > 0.5 else "失敗"
        return ScoreResult(score=score, success=success)

class ResponseCreator:
    def __init__(self, model: ChatVertexAI):
        self.model = model

    def run(self, score: float, base_response: str) -> str:
        prompt = ChatPromptTemplate([
            (
                "system",
                "あなたは告白に対する返事を作成する専門家です。スコアと結果に基づいて、相手の気持ちに配慮した自然な返事を作成してください。"
            ),
            (
                "human",
                "告白の返答のみを作成してください"
                "与えられた情報:\n評価結果: {result}\n感情スコア: {score}"
            )
        ])
        
        chain = prompt | self.model
        result = chain.invoke({"result": base_response, "score": score})
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
        print(f"入力テキスト: {text}")
        
        word_scores = vectorizer.run(text)
        print(word_scores.text)
        
        score_result = scorer.calculate_score(word_scores.scores)
        print(score_result.text)
        
        response = response_creator.run(score_result.score, score_result.success)
        print(f"返答: {response}")
        print("="*100)
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from model import Wordscore, ScoreResult
from typing import Dict, List

class ChatVectorizer:
    def __init__(self, model: ChatVertexAI):
        self.model = model
    
    def __parse_output(self, response : str)->List[Wordscore]:
        pairs = response.replace(" ", "").split(",")
        result = []
        for pair in pairs:
            key_value = pair.split(":")
            key = key_value[0].strip(' "')
            value = int(key_value[1].strip())
            result.append(Wordscore(word=key, score=value))
        return result

    def run(self, text: str) -> List[Wordscore]:
        prompt = ChatPromptTemplate([  # 感情分析のプロンプト
            (
                "system",
                "テキストから感情を表す単語を抽出し、ポジティブ/ネガティブの度合いを詳細に数値化してください。スコアは必ず-20から100の範囲で設定してください。"
            ),
            (
                "human",
                "抽出した単語はダブルクオートで囲み、「:」の後にそのスコアを記述してリストとして出力してください。"
                "コードブロックは使用しないでください"
                "以下のテキストを分析してください：{input_text}"
            )
        ])
        
        chain = prompt | self.model
        response: str = chain.invoke({"input_text": text}).content  # type:ignore
        result = self.__parse_output(response)
        return result



class ChatScorer:
    def calculate_score(self, word_scores: List[Wordscore]) -> ScoreResult:
        score = sum([ws.score for ws in word_scores]) / len(word_scores) if word_scores else 0.0
        success = "成功" if score > 50 else "失敗"
        return ScoreResult(score=score, success=success)

class ResponseCreator:
    def __init__(self, model: ChatVertexAI):
        self.model = model

    def run(self, score: float, base_response: str) -> str:
        prompt = ChatPromptTemplate([  # 返答生成のプロンプト
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
        # "好き。",
        "ずっと伝えたかったんだけど、あなたのことがとても好きです。もしよければ、これからもっと一緒に過ごしたいな。",
        "正直、もうこれ以上待てない気がする。ずっと好きだったけど、今まで何も言えなかった自分が情けなくて。"
    ]
    
    for text in sample_texts:
        print(f"入力テキスト: {text}")
        
        word_scores = vectorizer.run(text)
        print(f"感情スコア: {[f'{ws.word}: {ws.score}' for ws in word_scores]}")  # 出力を分かりやすく表示
        
        score_result = scorer.calculate_score(word_scores)
        print(score_result.text)
        
        response = response_creator.run(score_result.score, score_result.success)
        print(f"返答: {response}")
        print("="*100)



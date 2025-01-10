from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from src.agent.model import Persona


class Conversation:
    def __init__(self, model: ChatVertexAI, persona: Persona):
        self.model = model
        self.persona = persona

    def run(self, text: str) -> str:
        prompt = ChatPromptTemplate(
            [
                (
                    "system",
                    "あなたはペルソナになりきる専門家です。"
                    "過去の会話ログから会話に対する適切な応答をしてください。",
                ),
                (
                    "human",
                    "必ず会話の返答のみを返してください"
                    "ペルソナの情報：{persona}"
                    "会話:{input_text}",
                ),
            ]
        )

        chain = prompt | self.model
        response: str = chain.invoke(
            {"persona": self.persona.model_dump_json(), "input_text": text}
        ).content  # type:ignore
        return response

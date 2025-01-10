from langchain_google_vertexai import ChatVertexAI
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from src.agent.conv.conv_components import Conversation
from src.agent.conv.conv_state import State
from src.agent.model import Persona
import json


class ConversationAgent:
    def __init__(self, model_name: str, temperature: float, persona: Persona):
        self.model = ChatVertexAI(model_name=model_name, temperature=temperature)
        self.conversation_expert = Conversation(self.model, persona)

        self.memory = MemorySaver()
        self.graph_builder = StateGraph(State)
        self._create_graph()

    def _create_graph(self):
        """Set up the graph with nodes and edges."""

        def chatbot(state: State):
            user_message = state["messages"][-1].content
            return {"messages": [self.conversation_expert.run(user_message)]}

        self.graph_builder.add_node("chatbot", chatbot)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)
        self.graph = self.graph_builder.compile(checkpointer=self.memory)

    # def visualize_graph(self, output_path: str = "graph_visualization.png"):
    #     """Generate a visual representation of the graph."""
    #     graph_image = self.graph.get_graph().draw_mermaid_png()
    #     with open(output_path, "wb") as f:
    #         f.write(graph_image)

    def chat(self):
        """Interactive chat session."""
        print("Type 'quit', 'exit', or 'q' to end the conversation.\n")
        while True:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            self._stream_chat_updates(user_input)

    def _stream_chat_updates(self, user_input: str):
        """Stream and display chatbot responses."""
        for event in self.graph.stream(
            {"messages": [("user", user_input)]}, {"configurable": {"thread_id": "1"}}
        ):
            for value in event.values():
                print("Assistant:", value["messages"][-1])


def load_persona(path: str) -> Persona:
    # ペルソナのロードどこでやるか迷走中
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Persona(**data)


if __name__ == "__main__":
    persona = load_persona("src/agent/persona.json")
    chat_service = ConversationAgent(
        model_name="gemini-1.5-flash-002", temperature=0.0, persona=persona
    )
    chat_service.chat()

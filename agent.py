"""Minimal ReAct agent template for the AI Agents workshop.
You'll extend this in later labs.
"""
import os
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory

def create_agent():
    llm = ChatOpenAI(model_name="z-ai/glm-4.5-air:free", temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    tools = []  # You'll register a search tool in Lab 2
    agent = initialize_agent(
        tools,
        llm,
        agent="chat-zero-shot-react-description",
        memory=memory,
        verbose=True,
    )
    return agent

if __name__ == "__main__":
    agent = create_agent()
    print("Welcome to your ReAct agent. Type 'quit' to exit.")
    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            break
        if user_input.lower() in {'quit', 'exit'}:
            print("Goodbye!")
            break
        response = agent.run(user_input)
        print("Agent:", response)

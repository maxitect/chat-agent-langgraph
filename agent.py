"""Minimal ReAct agent template for the AI Agents workshop.
You'll extend this in later labs.
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import Tool
from langgraph.prebuilt import create_react_agent

# Load environment variables from .env file
load_dotenv()

def create_agent():
    llm = ChatOpenAI(model_name="z-ai/glm-4.5-air:free", temperature=0, base_url="https://openrouter.ai/api/v1")
    tools = []  # You'll register a search tool in Lab 2
    
    # Create ReAct agent with LangGraph (eliminates deprecation warnings)
    agent = create_react_agent(llm, tools)
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
        try:
            # LangGraph uses invoke with messages format
            response = agent.invoke({"messages": [("human", user_input)]})
            # Extract the final AI message from the response
            final_message = response["messages"][-1].content
            print("Agent:", final_message)
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")

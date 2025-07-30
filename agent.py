"""Minimal ReAct agent template for the AI Agents workshop.
You'll extend this in later labs.
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from tools.search import exa_search
from tools.add import add_function

# Load environment variables from .env file
load_dotenv()

def create_agent():
    llm = ChatOpenAI(model_name="qwen/qwen3-coder:free", temperature=0, base_url="https://openrouter.ai/api/v1")
    
    
    checkpointer = MemorySaver()

    tools = [add_function, exa_search]  # You'll register a search tool in Lab 2
    
    # Create ReAct agent with LangGraph
    agent = create_react_agent(llm, tools, checkpointer=checkpointer, verbose=True)
    

    #print(agent.get_graph().draw_mermaid_png())
    
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
            config = {"configurable": {"thread_id": "first_thread"}}


            # LangGraph uses invoke with messages format
            stream_mode = input("Enable streaming? (y/n): ").strip().lower() == "y"
            if stream_mode:
                for chunk in agent.stream({"messages": [("human", user_input)]}, config=config, stream_mode="updates"):
                    print(chunk)
                    print("--------------------------------")
            else:
                response = agent.invoke({"messages": [("human", user_input)]}, config=config, print_mode="tree")
                # Extract the final AI message from the response
                final_message = response["messages"][-1].content
                print("Agent:", final_message)


        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")

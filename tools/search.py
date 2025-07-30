"""Placeholder for a web search tool.
In Lab 2 you'll implement actual search functionality here.
"""
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_exa import ExaSearchResults
import os
from dotenv import load_dotenv

load_dotenv()


def duckduckgo_search(query: str) -> str:
    """Search the web using DuckDuckGo search API"""
    return  DuckDuckGoSearchRun(name="search-web")

def exa_search(query: str) -> str:
    """Search the web using Exa search API"""
    search_tool = ExaSearchResults(exa_api_key=os.environ["EXA_API_KEY"])

    search_results = search_tool._run(
    query=query,
    num_results=5,
    text_contents_options=True,
    highlights=True,
    )

    return search_results
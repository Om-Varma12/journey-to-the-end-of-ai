# tools/tavily_search.py

from tavily import TavilyClient
import os
from tool import Tool

class TavilySearchTool(Tool):
    def __init__(self):
        super().__init__(
            name="Web Search",
            desc="Search the web for real-time information"
        )
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def run(self, query: str) -> str:
        response = self.client.search(
            query=query,
            max_results=3,
            include_raw_content=True
        )

        results = []
        for r in response["results"]:
            results.append(
                f"Title: {r['title']}\n"
                f"Content: {r.get('content', '')}\n"
            )

        return "\n".join(results)
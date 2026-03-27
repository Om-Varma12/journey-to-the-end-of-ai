from ddgs import DDGS
from .base_tool import BaseTool


class WebSearchTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="web_search",
            description="Search the web for up-to-date information"
        )

    def run(self, query: str, max_results: int = 5):
        results = []

        try:
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=max_results):
                    results.append({
                        "title": r.get("title"),
                        "link": r.get("href"),
                        "snippet": r.get("body")
                    })

        except Exception as e:
            return [{
                "title": "ERROR",
                "link": "",
                "snippet": str(e)
            }]

        return results
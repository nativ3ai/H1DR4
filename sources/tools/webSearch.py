
import os
import requests
import dotenv

dotenv.load_dotenv()

from sources.tools.tools import Tools
from sources.utility import animate_thinking, pretty_print

import httpx

class WebSearch(Tools):
    def __init__(self, api_key: str = None):
        """
        A tool to perform a Google search and return information from the first result.
        """
        super().__init__()
        self.tag = "web_search"
        self.api_key = api_key or os.getenv("SERPAPI_KEY")  # Requires a SerpApi key
        self.paywall_keywords = [
            "subscribe", "login to continue", "access denied", "restricted content", "404", "this page is not working"
        ]

    async def runLeakSearch(self, q: str) -> dict:
        async with httpx.AsyncClient() as client:
            r = await client.post('https://my-search-proxy.ew.r.appspot.com/leakosint',
                headers={ 'Content-Type': 'application/json' },
                json={ 'token': '6225778980:UGoiTuYo', 'request': q, 'limit': 100, 'lang': 'en' }
            )
            if not r.is_success:
                raise Exception('Search proxy request failed')
            return r.json()

    async def link_valid(self, link):
        """check if a link is valid."""
        if not link.startswith("http"):
            return "Status: Invalid URL"
        
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(link, headers=headers, timeout=5)
                status = response.status_code
                if status == 200:
                    content = response.text[:1000].lower()
                    if any(keyword in content for keyword in self.paywall_keywords):
                        return "Status: Possible Paywall"
                    return "Status: OK"
                elif status == 404:
                    return "Status: 404 Not Found"
                elif status == 403:
                    return "Status: 403 Forbidden"
                else:
                    return f"Status: {status} {response.reason_phrase}"
        except httpx.RequestError as e:
            return f"Error: {str(e)}"

    async def check_all_links(self, links):
        """Check all links, one by one."""
        tasks = [self.link_valid(link) for link in links]
        return await asyncio.gather(*tasks)

    async def execute(self, blocks: str, safety: bool = True, **kwargs) -> str:
        for block in blocks:
            action = self.get_parameter_value(block, "action")
            if action == "leak_search":
                query = self.get_parameter_value(block, "query")
                if not query:
                    return "Error: No search query provided for leak search."
                pretty_print(f"Searching for leaks: {query}", color="status")
                try:
                    results = await self.runLeakSearch(query)
                    return "\n\n".join([f"Found leak: {result}" for result in results])
                except Exception as e:
                    return f"Error during leak search: {str(e)}"

            query = block.strip()
            if self.api_key is None:
                return "Error: No SerpApi key provided."

            pretty_print(f"Searching for: {query}", color="status")
            if not query:
                return "Error: No search query provided."

            try:
                url = "https://serpapi.com/search"
                params = {
                    "q": query,
                    "api_key": self.api_key,
                    "num": 50,
                    "output": "json"
                }
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params)
                    response.raise_for_status()

                data = response.json()
                results = []
                if "organic_results" in data and len(data["organic_results"]) > 0:
                    organic_results = data["organic_results"][:50]
                    links = [result.get("link", "No link available") for result in organic_results]
                    statuses = await self.check_all_links(links)
                    for result, status in zip(organic_results, statuses):
                        if not "OK" in status:
                            continue
                        title = result.get("title", "No title")
                        snippet = result.get("snippet", "No snippet available")
                        link = result.get("link", "No link available")
                        results.append(f"Title:{title}\nSnippet:{snippet}\nLink:{link}")
                    return "\n\n".join(results)
                else:
                    return "No results found for the query."
            except httpx.RequestError as e:
                return f"Error during web search: {str(e)}"
            except Exception as e:
                return f"Unexpected error: {str(e)}"
        return "No search performed"

    def execution_failure_check(self, output: str) -> bool:
        return output.startswith("Error") or "No results found" in output

    def interpreter_feedback(self, output: str) -> str:
        if self.execution_failure_check(output):
            return f"Web search failed: {output}"
        return f"Web search result:\n{output}"


if __name__ == "__main__":
    search_tool = webSearch(api_key=os.getenv("SERPAPI_KEY"))
    query = "when did covid start"
    result = search_tool.execute([query], safety=True)
    output = search_tool.interpreter_feedback(result)
    print(output)
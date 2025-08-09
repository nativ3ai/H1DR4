import os
import requests
from sources.tools.tools import Tools
from sources.utility import pretty_print

class Reasoning(Tools):
    def __init__(self):
        super().__init__()
        self.tag = "reasoning"
        self.name = "Reasoning"
        self.description = "A tool to perform complex reasoning tasks."
        self.url = "https://my-search-proxy.ew.r.appspot.com/reasoning"

    async def execute(self, blocks: str, context: list = None, safety: bool = True) -> str:
        for block in blocks:
            query = block.strip()
            pretty_print(f"Performing reasoning for: {query}", color="status")
            if not query:
                return "Error: No query provided."

            payload = {"query": query}
            if context:
                payload["context"] = context

            try:
                response = requests.post(self.url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("response", "No response from reasoning engine.")
            except requests.RequestException as e:
                return f"Error during reasoning request: {str(e)}"
            except Exception as e:
                return f"Unexpected error: {str(e)}"
        return "No reasoning performed"

    def execution_failure_check(self, output: str) -> bool:
        return output.startswith("Error") or "No response" in output

    def interpreter_feedback(self, output: str) -> str:
        if self.execution_failure_check(output):
            return f"Reasoning failed: {output}"
        return f"Reasoning result:\n{output}"

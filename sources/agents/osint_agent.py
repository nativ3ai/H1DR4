import asyncio

from sources.utility import pretty_print, animate_thinking
from sources.agents.agent import Agent
from sources.tools.webSearch import WebSearch
from sources.memory import Memory

class OsintAgent(Agent):
    def __init__(self, name, prompt_path, provider, verbose=False):
        """
        The OSINT agent is a special agent for searching leaks.
        """
        super().__init__(name, prompt_path, provider, verbose, None)
        self.tools = {
            "web_search": WebSearch()
        }
        self.role = "osint"
        self.type = "osint_agent"
        self.memory = Memory(self.load_prompt(prompt_path),
                        recover_last_session=False,
                        memory_compression=False,
                        model_provider=provider.get_model_name())

    async def process(self, prompt, speech_module) -> str:
        exec_success = False
        self.memory.push('user', prompt)
        while exec_success is False and not self.stop:
            await self.wait_message(speech_module)
            animate_thinking("Thinking...", color="status")
            answer, reasoning = await self.llm_request()
            self.last_reasoning = reasoning
            exec_success, _ = self.execute_modules(answer)
            answer = self.remove_blocks(answer)
            self.last_answer = answer
        self.status_message = "Ready"
        return answer, reasoning

if __name__ == "__main__":
    pass

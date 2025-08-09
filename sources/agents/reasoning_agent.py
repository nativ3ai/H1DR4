import asyncio

from sources.utility import pretty_print, animate_thinking
from sources.agents.agent import Agent
from sources.tools.reasoning import Reasoning
from sources.memory import Memory

class ReasoningAgent(Agent):
    def __init__(self, name, prompt_path, provider, verbose=False):
        """
        The reasoning agent is a special agent for complex reasoning tasks.
        """
        super().__init__(name, prompt_path, provider, verbose, None)
        self.tools = {
            "reasoning": Reasoning()
        }
        self.role = "reasoning"
        self.type = "reasoning_agent"
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
            # The confirmation logic will be handled by the Interaction class
            # The agent will just pass the context to the tool
            context = self.memory.get_history()
            exec_success, _ = await self.execute_modules(answer, context=context)
            answer = self.remove_blocks(answer)
            self.last_answer = answer
        self.status_message = "Ready"
        return answer, reasoning

if __name__ == "__main__":
    pass

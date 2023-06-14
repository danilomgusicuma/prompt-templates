from typing import List, Optional
from abc import ABC, abstractmethod

from prompt_templates.mem_prompt.prompt_template import DEFAULT_MEM_PROMPT_TEMPLATE
from models.memory_item import MemoryItem


class BaseMemPrompt(ABC):
    """Base class for memory prompts that provide completion functionality based on memory.

    This class defines the basic structure and behavior for memory prompts. It allows retrieving memory,
    saving memory, and completing prompts with the available memory.

    Methods:
        get_memory(): Abstract method to retrieve memory from a specific source.
        save_memory(memory: List[MemoryItem]): Abstract method to save memory to a specific destination.
        complete_prompt(current_question: str) -> str: Completes the prompt with the available memory.
    """
    def __init__(self, prompt_template: str = DEFAULT_MEM_PROMPT_TEMPLATE):
        self._prompt_template = prompt_template

    @abstractmethod
    def get_memory(self) -> Optional[List[MemoryItem]]:
        pass

    @abstractmethod
    def save_memory(self, memory: List[MemoryItem]) -> None:
        pass

    def complete_prompt(self, current_question: str) -> str:
        """
        Complete the prompt with the available memory.

        If memory is available, it generates a completed prompt by inserting the current question
        and the history section from the memory into the prompt template. If memory is not available,
        it returns the current question itself.

        Args:
            current_question (str): The current question prompt.

        Returns:
            str: The completed prompt.

        """
        memory = self.get_memory()

        if not memory:
            return current_question

        history_section = "\n".join(
            [
                f"question: {m.question}\nanswer: {m.answer}\n"
                for m in memory
            ]
        )

        completed_prompt = self._prompt_template.format(
            current_question=current_question,
            history_section=history_section
        )

        return completed_prompt


if __name__ == "__main__":
    class SimpleMemPrompt(BaseMemPrompt):
        def get_memory(self) -> Optional[List[MemoryItem]]:
            custom_memory = [
                MemoryItem(question="How many apples does Mary have?", answer="Mary has two apples"),
                MemoryItem(question="How many apples does John have?", answer="John has four apples"),
            ]
            return custom_memory

        def save_memory(self, memory: List[MemoryItem]) -> None:
            pass
    completer = SimpleMemPrompt()
    print(completer.complete_prompt("How many apples do Mary and John have together?"))

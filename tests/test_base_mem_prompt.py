import unittest
from typing import List, Optional

from models.memory_item import MemoryItem
from prompt_templates.mem_prompt.base_mem_prompt import BaseMemPrompt


class MockMemPrompt(BaseMemPrompt):
    def __init__(self, memory: Optional[List[MemoryItem]] = None):
        super().__init__()
        self.memory = memory

    def get_memory(self) -> Optional[List[MemoryItem]]:
        return self.memory

    def save_memory(self, memory: List[MemoryItem]) -> None:
        self.memory = memory


class BaseMemPromptTests(unittest.TestCase):
    def setUp(self):
        self.prompt = MockMemPrompt()

    def test_complete_prompt_with_empty_memory(self):
        current_question = "How many apples Mary and John have together?"
        completed_prompt = self.prompt.complete_prompt(current_question)
        self.assertEqual(completed_prompt, current_question)

    def test_complete_prompt_with_memory(self):
        memory = [
            MemoryItem(question="How many apples does Mary have?", answer="Mary has two apples"),
            MemoryItem(question="How many apples does John have?", answer="John has four apples"),
        ]
        self.prompt.save_memory(memory)

        current_question = "How many apples Mary and John have together?"
        expected_prompt = """\
In order to answer the CURRENT_QUESTION, you have to take into consideration the questions and answers in the HISTORY
section.

--------
HISTORY:

question: How many apples does Mary have?
answer: Mary has two apples

question: How many apples does John have?
answer: John has four apples

--------
CURRENT_QUESTION: {current_question}
CURRENT_ANSWER: \
""".format(current_question=current_question)

        completed_prompt = self.prompt.complete_prompt(current_question)
        self.assertEqual(completed_prompt, expected_prompt)


if __name__ == "__main__":
    unittest.main()

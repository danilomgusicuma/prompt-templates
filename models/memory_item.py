from pydantic import BaseModel


class MemoryItem(BaseModel):
    question: str
    answer: str

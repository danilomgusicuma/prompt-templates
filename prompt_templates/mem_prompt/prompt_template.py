DEFAULT_MEM_PROMPT_TEMPLATE = """\
In order to answer the CURRENT_QUESTION, you have to take into consideration the questions and answers in the HISTORY
section.

--------
HISTORY:

{history_section}
--------
CURRENT_QUESTION: {current_question}
CURRENT_ANSWER: \
"""

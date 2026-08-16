from typing import Literal

from pydantic import BaseModel


# Это Политех такие шикарные имена для полей выдумал
class Candidate(BaseModel):
    num: int
    code: str
    sum: int
    # До булевого типа не додумались
    agreement: Literal["Получено", "Отсутствует"]
    primary_highest_priority: Literal["Да", None]
    highest_passing_priority: Literal["Да", None]
    comment_status: Literal[
        "К зачислению",
        "В резерве к зачислению",
        "К зачислению по другому приоритету",
        "Участвует в конкурсе"
    ]

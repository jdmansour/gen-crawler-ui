from enum import Enum


class GetPredefinedPromptForCollectionMode(str, Enum):
    QUESTIONANSWER = "QuestionAnswer"
    SUMMARY = "Summary"

    def __str__(self) -> str:
        return str(self.value)

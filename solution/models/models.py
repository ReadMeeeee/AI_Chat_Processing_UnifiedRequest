from pydantic import BaseModel


class Message(BaseModel):
    sender: str
    text: str


class Chat(BaseModel):
    messages: list[Message]
    name: str = None
    numbers: list[str] | set[str] = None


class CompanyChat(BaseModel):
    company: str
    whole_chat: str


class Instruction(BaseModel):
    instruction: str
    example: str = ""
    response_format: str = ""


    def unit_it(self) -> str:
        s = (f"{self.instruction}\n"
             f"Пример для выполнения задачи:\n{self.example}\n"
             f"Формат вывода:\n{self.response_format}\n")
        return s


class InstructionBlock(BaseModel):
    role: str
    introduction: str
    instructions: str | None
    context: str | None
    format: str | None


class LLMRequest(BaseModel):
    instruction_block: InstructionBlock
    task: str


    def to_prompt(self) -> list[dict[str, str]]:

        instructions = f"{self.instruction_block.introduction}\n\n{self.instruction_block.instructions}\n"

        content = (
            f"Инструкции:\n{instructions}\n\n"
            f"Контекст:\n{self.instruction_block.context}\n\n"
            f"Формат вывода:\n{self.instruction_block.format}\n\n"
            f"Входные данные:\n{self.task}"
        )
        return [
            {"role": "system", "content": self.instruction_block.role},
            {"role": "user", "content": content}
        ]

class ProblemWithSolution(BaseModel):
        description: str
        keywords: list[str]
        solution: str
        name: str = "untitled"
        numbers: list[str] = None

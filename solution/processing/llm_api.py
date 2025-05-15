from os import path
from json import loads, JSONDecodeError
from openai import OpenAI

from solution.models import LLMRequest, ProblemWithSolution
from solution.file_io import load_data, load_instruction_file


class AIModelAPI:
    def __init__(self, api: str, url: str, model_name: str):
        self.api = api
        self.url = url
        self.model_name = model_name
        self.client = OpenAI(api_key=self.api, base_url=self.url)

    def get_response(self, request: LLMRequest,
                     temperature: float = 0.1):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=request.to_prompt(),
            stream=False,
            temperature=temperature
        )
        return response.choices[0].message.content


def chat_process(
        model: AIModelAPI,
        path_to_instruct_json: str,
        path_to_task_txt: str,
) -> ProblemWithSolution:

    name = path.splitext(path.basename(path_to_task_txt))[0]
    general_task = load_data(path_to_task_txt)
    instructions = load_instruction_file(path_to_instruct_json)
    req = LLMRequest(instruction_block=instructions, task=general_task)

    try:
        result_text = model.get_response(req)
    except Exception as e:
        raise RuntimeError(f"Ошибка при обращении к ИИ: {e}")

    try:
        result_dict = loads(result_text)
    except JSONDecodeError as e:
        raise ValueError(f"Ответ ИИ не является корректным JSON: {e}\nОтвет: {result_text}")

    return ProblemWithSolution(
        name=name,
        description=result_dict.get("description", ""),
        keywords=result_dict.get("keywords", []),
        solution=result_dict.get("solution", "")
    )
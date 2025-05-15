from json import load, dump
from os import path
from solution.models import Instruction, InstructionBlock, ProblemWithSolution


def _is_file_is_correct(path_to_file: str, file_format: str, is_file: bool = True, is_correct: bool = True) -> None:
    if is_file and not path.exists(path_to_file):
        raise FileNotFoundError(f"Файл не найден: {path_to_file}")

    if is_correct and not file_format.startswith("."):
        raise ValueError(f"Аргумент 'file_format' должен начинаться с точки. Получено: \"{file_format}\"")

    shaped_path = path.splitext(path.basename(path_to_file))
    format_of_file = shaped_path[1]

    if is_correct and format_of_file != file_format:
        raise ValueError(f"Ожидаемый формат файла - \"{file_format}\", получен - {format_of_file}")


def load_data(txt_task_path: str) -> str:
    _is_file_is_correct(txt_task_path, ".txt")
    with open(txt_task_path, "r", encoding="utf-8") as f:
        return f.read()


def load_instruction_file(json_instruction_path: str) -> InstructionBlock:
    _is_file_is_correct(json_instruction_path, ".json")
    with open(json_instruction_path, "r", encoding="utf-8") as f:
        data = load(f)


    def _is_subset_of(keys: set[str], data_position: dict) -> None:
        if not keys.issubset(data_position):
            raise KeyError(f"Инструкции не содержат необходимые ключи: {keys - set(data_position)}")


    paragraph_keys = {"role", "introduction", "context", "instructions", "output_format"}
    instruction_keys = {"description", "keywords", "solution"}
    for_instruction_keys = {"instruction", "example", "response_format"}

    _is_subset_of(paragraph_keys, data)
    _is_subset_of(instruction_keys, data['instructions'])
    _is_subset_of(for_instruction_keys, data['output_format'])
    for item in data['instructions']:
        _is_subset_of(for_instruction_keys, data['instructions'][item])


    def make_instruction(data_section: dict[str, dict], key_of_section: str) -> str:
        subdata = data_section[key_of_section]
        instruction = Instruction(
            instruction=subdata.get("instruction", ""),
            example=subdata.get("example", ""),
            response_format=subdata.get("response_format", ""),
        )
        return instruction.unit_it()


    instructions = ""
    for key in instruction_keys:
        instruct = make_instruction(data["instructions"], key)
        instructions += f"{instruct}\n"

    format_instruction = make_instruction({"output_format": data["output_format"]}, "output_format")

    return InstructionBlock(
        role=data["role"],
        introduction=data["introduction"],
        instructions=instructions,
        context="\n".join(data["context"]) if isinstance(data["context"], list) else data["context"],
        format=format_instruction
    )


def upload_data(json_solution_path: str, list_of_sol: list[ProblemWithSolution]):
    _is_file_is_correct(json_solution_path, ".json", is_file = False)

    sol_json: list[dict] = []
    for sol in list_of_sol:
        str_to_write = {
            "company": sol.name,
            "description": sol.description,
            "keywords": sol.keywords,
            "solution": sol.solution
        }

        sol_json.append(str_to_write)

    with open(json_solution_path, "w", encoding="utf-8") as f:
        dump(sol_json, f, ensure_ascii=False, indent=4)


"""
def main():
    from solution.config import path_to_instruct_json


    instructs = load_instruction_file(path_to_instruct_json)
    instructions = f"{instructs.introduction}\n\n{instructs.instructions}\n"
    print(f"role:         {instructs.role}\n\n"
          f"instructions: {instructions}\n\n"
          f"context:      {instructs.context}\n\n"
          f"format:       {instructs.format}\n\n"  )

    return None


if __name__ == "__main__":
    main()
"""

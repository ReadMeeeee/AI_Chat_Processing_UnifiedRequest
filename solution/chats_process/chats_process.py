from os import path

from solution.processing import AIModelAPI, chat_process, process_all_docs
from solution.file_io import upload_data
from solution.models import ProblemWithSolution


def process_all_chats(
        model: {AIModelAPI, str, str},
        path_to_input: str,
        path_to_process: str,
        path_to_instruct: str,
        path_to_output: str
) -> None:

    company_chats = process_all_docs(path_to_input, output_dir=path_to_process)

    if not company_chats:
        print("Нет данных для обработки.")
        return None

    list_of_sol: list[ProblemWithSolution] = []
    for company in company_chats:
        task_filename = f"{company.company}.txt"
        path_to_task_txt = path.join(path_to_process, task_filename)

        try:
            sol = chat_process(
                model=model,
                path_to_instruct_json=path_to_instruct,
                path_to_task_txt=path_to_task_txt,
            )
            list_of_sol.append(sol)

        except FileNotFoundError:
            print(f"Файл не найден: {path_to_task_txt}")
        except Exception as e:
            print(f"Ошибка при обработке {company.company}: {e}")

    if list_of_sol:
        upload_data(json_solution_path=path_to_output, list_of_sol=list_of_sol)
    else:
        print("Нет решений для записи.")

    return None
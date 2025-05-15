from solution.file_io import load_docx_from_project, ensure_folder_exists, write_text_to_file
from solution.processing import convert_from_docx, format_chat
from solution.models import Chat, CompanyChat


def process_all_docs(path_to_input_data: str, output_dir: str = None) -> list[CompanyChat]:
    docs = load_docx_from_project(path_to_input_data)

    chats: list[Chat] = [convert_from_docx(doc) for doc in docs]
    company_chats: list[CompanyChat] = [format_chat(chat) for chat in chats]

    ensure_folder_exists(output_dir)
    for data in company_chats:
        write_text_to_file(data, output_dir)

    return company_chats
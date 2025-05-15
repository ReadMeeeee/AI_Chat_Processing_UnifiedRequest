from os import listdir, path
from docx import Document


def load_docx_from_project(path_in_project='input_data/') -> list[tuple[str, Document]]:
    documents = []

    if not path.exists(path_in_project) or not path.isdir(path_in_project):
        print(f"Директория не найдена: {path_in_project}")
        return []

    for filename in listdir(path_in_project):
        if filename.endswith('.docx'):
            full_path = path.join(path_in_project, filename)
            try:
                document = Document(full_path)
                documents.append([filename, document])
            except Exception as e:
                print(f"Не удалось загрузить {filename}: {e}")

    return documents

from docx import Document
from solution.models import Message, Chat, CompanyChat
from solution.processing import REMOVE_CHARS, clear_text


def convert_from_docx(document: tuple[str, Document]):
    name = document[0][:-5]

    table = document[1].tables[0]
    numbers: list[str] = []
    messages: list[Message] = []
    for row in table.rows[1:]:
        cells = row.cells
        message = Message(sender=cells[1].text, text=cells[2].text)

        numbers.append(cells[0].text)
        messages.append(message)

    chat = Chat(
        name=name,
        numbers=set(numbers),
        messages=messages
    )
    '''
    print(f"|{'Компания':<16}|", chat.name,
          f"\n|{'№ обращений':<16}|", chat.numbers,
          f"\n|{'Отправитель':<16}|", chat.messages[0].sender,
          f"\n|{'Текст сообщения':<16}|\n", chat.messages[0].text)
    '''
    return chat


def format_chat(chat: Chat) -> CompanyChat:
    dialog = ""

    for message in chat.messages:
        cleared_text = clear_text(message.text, REMOVE_CHARS)
        dialog += (message.sender + ': ' + '\n' +
                   cleared_text + '\n\n')

    name_data = CompanyChat(company=chat.name, whole_chat=dialog)
    return name_data
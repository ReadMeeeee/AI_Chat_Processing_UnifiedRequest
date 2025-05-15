from re import sub


REMOVE_CHARS = {
    0x00A0: None,  # NBSP – неразрывный пробел
    0x00AD: None,  # SHY – мягкий перенос
    0x200B: None,  # ZWSP – нулевой пробел
    0xFEFF: None   # BOM – метка порядка байтов
}


def clear_text(
    text: str,
    symbols_to_remove: dict[int, None],
    to_lower: bool = False,
    normalize_spaces: bool = True
) -> str:
    text = text.translate(symbols_to_remove)
    text = sub(r'\n+', '\n', text)
    text = sub(r'[ \t]+\n', '\n', text)

    if normalize_spaces:
        text = sub(r'[ \t]{2,}', ' ', text)

    text = "\n".join(line.strip() for line in text.splitlines())

    if to_lower:
        text = text.lower()

    return text.strip()

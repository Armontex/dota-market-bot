# NOTESTED
def cut_to_length(text: str, length: int) -> str:
    """Обрезает текст до указанной длины и добавляет многоточие.

    Args:
        text (str): Исходный текст для обрезки.
        length (int): Максимальная длина текста (без учета многоточия).

    Returns:
        str: Обрезанный текст с добавленным многоточием в конце.
        
    Example:
        >>> cut_to_length("Длинный текст сообщения", 8)
        'Длинный ...'
    """
    return text[:length] + "..."

DISALLOWED_CHARS = "!\"#$%&'()*+,:;<=>?@[\\]^`{|}~"


def string_is_valid(string: str, disallowed_chars: str = DISALLOWED_CHARS) -> None | str:
    """Check if a string contains disallowed characters.

    Args:
        string (str): The string to check.
        disallowed_chars (str): A string containing all disallowed characters.

    Returns:
        bool: True if the string is valid, False otherwise.
    """
    for c in string:
        if c in disallowed_chars:
            return c
    return None

import string


def without_whitespace(text):
    if len(text) == 0:
        return False

    for i in text:
        if i in string.whitespace:
            return False
    return True
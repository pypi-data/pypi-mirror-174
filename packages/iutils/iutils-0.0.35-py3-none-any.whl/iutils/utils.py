def remove_last_n_chars(string: str, n: int):
    """Given a string, return the string with its last n characters removed."""
    if type(n) is not int:
        raise TypeError(f"`{n}' must be an integrer.")

    if n < 0:
        raise ValueError(f"`{n}' must be greater than or equal to 0.")

    if len(string) <= n:
        return ""

    return string[: len(string) - n]


def two_level_split(line, sep=" ", quote='"'):
    """Split a line by sep.

    The line may optionally contains fields that are quoted by the quote sign.
    """

    in_quotes = False
    results = []
    temp = []

    for field in line.split(sep):
        if not field:
            # append to temp if in_quotes, otherwise append to results
            temp.append(field) if in_quotes else results.append(field)
            continue

        if in_quotes:
            if field[0] == quote:
                raise ValueError(f"Non-matching `{quote}' quote: {line}")
            else:
                if field[-1] == quote:
                    temp.append(field.strip(quote))
                    results.append(sep.join(temp))
                    temp = []
                    in_quotes = False
                else:
                    temp.append(field)
        else:
            if field[0] == quote:
                if field[-1] == quote:
                    results.append(field.strip(quote))
                else:
                    in_quotes = True
                    temp.append(field.strip(quote))
            else:
                if field[-1] == quote:
                    raise ValueError(f"Non-matching `{quote}' quote: {line}")
                else:
                    results.append(field)

    return results

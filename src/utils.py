def check(condition: bool, message: str):
    if not condition:
        raise ValueError(message)

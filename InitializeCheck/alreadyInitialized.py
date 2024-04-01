from typing import Any


def alreadyInitialized(variable: Any, name: str) -> None:
    if variable is not None:
        raise Exception(f'You can\'t change "{name}" value after it\'s been initialized.')

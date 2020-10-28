from random import choice
from string import ascii_lowercase


def generate_id() -> str:
    def chars(n: int) -> str:
        return "".join(choice(ascii_lowercase) for _ in range(n))

    return f"{chars(3)}-{chars(4)}-{chars(3)}"

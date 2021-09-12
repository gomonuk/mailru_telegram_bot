from dotenv import load_dotenv

load_dotenv()


def check(in_str: str) -> bool:
    return bool(in_str)


def calc(string: str) -> int:
    return eval(string)

from typing import Tuple

OPEN_BRACKET = "("
CLOSE_BRACKET = ")"
PRIORITY_MAP = {
    OPEN_BRACKET: 0,
    CLOSE_BRACKET: 1,
    "+": 2,
    "-": 2,
    "/": 3,
    "*": 3,
}

OPERATOR_MAP = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "/": lambda x, y: x / y,
    "*": lambda x, y: x * y,
}

bad_brackets_error = Exception("У вас скобочка не закрыта :)")


def string_normalization(string: str) -> Tuple[list, Exception]:
    bracket_count = 0
    out = []
    error = None
    for item in string:
        if item.isdigit() or item in PRIORITY_MAP.keys():
            out.append(item)

        if item == OPEN_BRACKET:
            bracket_count += 1

        if item == CLOSE_BRACKET:
            bracket_count -= 1

    if bracket_count != 0:
        error = bad_brackets_error

    return out, error


def create_rpn(expression: list):
    """
    Полное описание алгоритма:
    https://ru.wikipedia.org/wiki/%D0%9E%D0%B1%D1%80%D0%B0%D1%82%D0%BD%D0%B0%D1%8F_%D0%BF%D0%BE%D0%BB%D1%8C%D1%81%D0%BA%D0%B0%D1%8F_%D0%B7%D0%B0%D0%BF%D0%B8%D1%81%D1%8C

    Краткая выжимка:
    Пока есть ещё символы для чтения:
        1. Читаем очередной символ.
            1.1 Если символ является числом добавляем его к выходной строке.
            1.2 Если символ является открывающей скобкой, помещаем его в стек.
            1.3 Если символ является закрывающей скобкой:
                    До тех пор, пока верхним элементом стека не станет открывающая скобка,
                    выталкиваем элементы из стека в выходную строку.
                    При этом открывающая скобка удаляется из стека, но в выходную строку не добавляется.
            1.4 Если символ является бинарной операцией о1, тогда:
                1.4.1 операция на вершине стека приоритетнее o1 выталкиваем
                      верхний элемент стека в выходную строку;
                1.4.2 помещаем операцию o1 в стек.
        2. Когда входная строка закончилась, выталкиваем все символы из стека в выходную строку.
           В стеке должны были остаться только символы операций; если это не так, значит в выражении не согласованы скобки.
    """
    stack = []
    out = []

    for item in expression:  # 1.1
        if item.isdigit():
            out.append(int(item))
            continue

        if not stack or item == OPEN_BRACKET:  # 1.2
            stack.append(item)
            continue

        if item == CLOSE_BRACKET:  # 1.3
            for _ in reversed(stack):
                operator = stack.pop()
                if operator != OPEN_BRACKET:
                    out.append(operator)
                else:
                    break
            continue
        else:  # 1.4
            for operator in reversed(stack):  # 1.4.1
                if PRIORITY_MAP[operator] < PRIORITY_MAP[item]:
                    break
                out.append(stack.pop())

            stack.append(item)  # 1.4.2

    for _ in range(len(stack)):  # 2.
        out.append(stack.pop())

    return out


def exec_rpn(rpn_expression: list) -> int:
    stack = []
    for item in rpn_expression:
        if isinstance(item, int):
            stack.append(item)
            continue

        operand_left, operand_right = stack.pop(), stack.pop()
        operator = OPERATOR_MAP[item]
        stack.append(operator(operand_left, operand_right))

    assert len(stack) == 1, stack
    return stack[0]

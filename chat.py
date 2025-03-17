import re
from abc import ABC, abstractmethod
from typing import List, Callable


class Operator(ABC):
    def __init__(self, symbol: str, precedence: int, arity: int):
        self.symbol = symbol
        self.precedence = precedence
        self.arity = arity

    @abstractmethod
    def evaluate(self, *args: float) -> float:
        pass


class Fraction(Operator):
    def __init__(self):
        super().__init__('!', 7, 1)

    def evaluate(self, x: float) -> float:
        return 1 / x if x != 0 else float('inf')


class Negative(Operator):
    def __init__(self):
        super().__init__('~', 6, 1)

    def evaluate(self, x: float) -> float:
        return -x


class Max(Operator):
    def __init__(self):
        super().__init__('@', 5, 2)

    def evaluate(self, x: float, y: float) -> float:
        return max(x, y)


class Min(Operator):
    def __init__(self):
        super().__init__('&', 5, 2)

    def evaluate(self, x: float, y: float) -> float:
        return min(x, y)


class Average(Operator):
    def __init__(self):
        super().__init__('$', 5, 2)

    def evaluate(self, x: float, y: float) -> float:
        return (x + y) / 2


class Modulo(Operator):
    def __init__(self):
        super().__init__('%', 4, 2)

    def evaluate(self, x: float, y: float) -> float:
        return x % y


class Power(Operator):
    def __init__(self):
        super().__init__('^', 3, 2)

    def evaluate(self, x: float, y: float) -> float:
        return x ** y


class Multiply(Operator):
    def __init__(self):
        super().__init__('*', 3, 2)

    def evaluate(self, x: float, y: float) -> float:
        return x * y


class Divide(Operator):
    def __init__(self):
        super().__init__('/', 3, 2)

    def evaluate(self, x: float, y: float) -> float:
        return x / y if y != 0 else float('inf')


class Add(Operator):
    def __init__(self):
        super().__init__('+', 1, 2)

    def evaluate(self, x: float, y: float) -> float:
        return x + y


class Subtract(Operator):
    def __init__(self):
        super().__init__('-', 1, 2)

    def evaluate(self, x: float, y: float) -> float:
        return x - y


class Calculator:
    def __init__(self):
        self.operators = {
            '!': Fraction(), '~': Negative(), '@': Max(), '&': Min(), '$': Average(),
            '%': Modulo(), '^': Power(), '*': Multiply(), '/': Divide(), '+': Add(), '-': Subtract()
        }

    def evaluate(self, expression: str) -> float:
        tokens = self.tokenize(expression)
        postfix = self.to_postfix(tokens)
        return self.compute_postfix(postfix)

    def tokenize(self, expression: str) -> List[str]:
        return re.findall(r'\d+|[!~@&$%^*/+-]', expression)

    def to_postfix(self, tokens: List[str]) -> List[str]:
        output, stack = [], []
        for token in tokens:
            if token.isdigit():
                output.append(token)
            elif token in self.operators:
                while (stack and stack[-1] in self.operators and
                       self.operators[stack[-1]].precedence >= self.operators[token].precedence):
                    output.append(stack.pop())
                stack.append(token)
        while stack:
            output.append(stack.pop())
        return output

    def compute_postfix(self, postfix: List[str]) -> float:
        stack = []
        for token in postfix:
            if token.isdigit():
                stack.append(float(token))
            elif token in self.operators:
                operator = self.operators[token]
                args = [stack.pop() for _ in range(operator.arity)][::-1]
                stack.append(operator.evaluate(*args))
        return stack[0] if stack else 0


if __name__ == "__main__":
    calculator = Calculator()
    expr = "~-5+90"
    result = calculator.evaluate(expr)
    print(f"Result: {result}")

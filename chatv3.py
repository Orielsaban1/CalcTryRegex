import re
import math
from abc import ABC, abstractmethod
from typing import List


# -------------------------------
# הגדרת האופרטורים
# -------------------------------

class Operator(ABC):
    def __init__(self, symbol: str, precedence: int, arity: int, right_association : bool = False):
        self.symbol = symbol
        self.precedence = precedence
        self.arity = arity
        self.right_association  = right_association 

    @abstractmethod
    def evaluate(self, *args: float) -> float:
        pass


class Factorial(Operator):
    def __init__(self):
        super().__init__('!', 7, 1, True)

    def evaluate(self, x: float) -> float:
        # עצרת מוגדרת עבור מספרים לא שליליים (כולל עשרוניים)
        if x < 0:
            raise ValueError("Factorial is only defined for non-negative numbers.")
        # math.gamma(x+1) נותן את העצרת עבור x (גם עבור ערכים עשרוניים)
        return math.gamma(x + 1)


class Negative(Operator):
    def __init__(self):
        super().__init__('~', 6, 1, True)

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
        if y!=0: return x/y
        else:
            raise TypeError("Division is only defined for non-zero numbers.")


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


# -------------------------------
# הגדרת צמתי העץ (AST)
# -------------------------------

class Node(ABC):
    @abstractmethod
    def evaluate(self) -> float:
        pass


class NumberNode(Node):
    def __init__(self, value: float):
        self.value = value

    def evaluate(self) -> float:
        return self.value


class UnaryOpNode(Node):
    def __init__(self, op: Operator, child: Node):
        self.op = op
        self.child = child

    def evaluate(self) -> float:
        return self.op.evaluate(self.child.evaluate())


class BinaryOpNode(Node):
    def __init__(self, op: Operator, left: Node, right: Node):
        self.op = op
        self.left = left
        self.right = right

    def evaluate(self) -> float:
        return self.op.evaluate(self.left.evaluate(), self.right.evaluate())


# -------------------------------
# Parser: בניית העץ לפי סדר העדיפויות
# -------------------------------

class Parser:
    def __init__(self, tokens: List[str], operators: dict):
        self.tokens = tokens
        self.pos = 0
        self.operators = operators

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self):
        self.pos += 1

    def parse(self) -> Node:
        return self.parse_expression(0)

    def parse_primary(self) -> Node:
        token = self.current()
        if token is None:
            raise Exception('Unexpected end of input')
        if token == '(':
            self.consume()
            node = self.parse_expression(0)
            if self.current() != ')':
                raise Exception('Missing closing parenthesis')
            self.consume()  # Consume ')'
            return node
        # טיפול באופרטור חד־ערכי (prefix) – למשל, ~
        if token in self.operators and self.operators[token].arity == 1 and token not in ['!']:
            op = self.operators[token]
            self.consume()
            child = self.parse_expression(op.precedence)
            return UnaryOpNode(op, child)
        # צפוי מספר (כולל מספר עם מינוס כחלק מהליטרל)
        try:
            value = float(token)
            self.consume()
            return NumberNode(value)
        except ValueError:
            raise Exception(f'Invalid token: {token}')

    def parse_expression(self, min_prec: int) -> Node:
        left = self.parse_primary()
        # טיפול באופרטורים חד־ערכיים בצורה postfix (כמו עצרת !)
        while self.current() in self.operators and self.operators[self.current()].arity == 1 and self.current() == '!':
            op = self.operators[self.current()]
            self.consume()
            left = UnaryOpNode(op, left)
        while True:
            token = self.current()
            if token is None or token not in self.operators or self.operators[token].arity != 2:
                break
            op = self.operators[token]
            prec = op.precedence
            assoc = 'right' if op.right_association  else 'left'
            if prec < min_prec:
                break
            self.consume()
            next_min = prec + 1 if assoc == 'left' else prec
            right = self.parse_expression(next_min)
            left = BinaryOpNode(op, left, right)
            # טיפול באופרטור postfix נוסף אם קיים
            while self.current() in self.operators and self.operators[
                self.current()].arity == 1 and self.current() == '!':
                op_post = self.operators[self.current()]
                self.consume()
                left = UnaryOpNode(op_post, left)
        return left


# -------------------------------
# פונקציית טוקניזציה מותאמת
# -------------------------------

def tokenize(expression: str) -> List[str]:
    """
    מפצלת את הביטוי לטוקנים.
    כלל מיוחד: אם מופיע סימן '-' בתחילת הביטוי או לאחר אופרטור/סוגר פתיחה, הוא ישויך כחלק מהמספר.
    בנוסף, אם מופיע '-' אחרי '~' כאשר מיד אחריו מגיע מספר עם עצרת, נטפל במצב בצורה מתאימה.
    """
    tokens = []
    i = 0
    expr = expression.replace(' ', '')
    while i < len(expr):
        ch = expr[i]
        if ch.isdigit() or (ch == '.' and i + 1 < len(expr) and expr[i + 1].isdigit()):
            num = ch
            i += 1
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                num += expr[i]
                i += 1
            tokens.append(num)
        elif ch == '-':
            # אם אין טוקן קודם או שהקודם הוא סוגר פתיחה או אופרטור, נחבר את '-' לחלק מהמספר
            if not tokens or tokens[-1] in ['(', '+', '-', '*', '/', '!', '@', '&', '$', '%', '^', '~']:
                num = ch
                i += 1
                while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                    num += expr[i]
                    i += 1
                tokens.append(num)
            else:
                tokens.append(ch)
                i += 1
        else:
            tokens.append(ch)
            i += 1
    return tokens


# -------------------------------
# מחלקת המחשבון שמשתמשת ב-AST
# -------------------------------

class Calculator:
    def __init__(self):
        self.operators = {
            '!': Factorial(), '~': Negative(), '@': Max(), '&': Min(), '$': Average(),
            '%': Modulo(), '^': Power(), '*': Multiply(), '/': Divide(), '+': Add(), '-': Subtract()
        }

    def evaluate(self, expression: str) -> float:
        tokens = tokenize(expression)
        parser = Parser(tokens, self.operators)
        ast = parser.parse()
        return ast.evaluate()


# -------------------------------
# בדיקות והדפסת תוצאות
# -------------------------------

if __name__ == '__main__':
    calculator = Calculator()

    expr1 = '~-5+90'  # ~(-5) = 5, ואז 5+90 = 95.
    expr2 = '~-10 + 4!'  # בתוך הסוגריים: -50+95*8 = 710; לאחר מכן: 710-20 = 690; ואז: 690+(~50) כאשר ~50 = -50 → 640.
    expr3 = '5!'  # 5! = 120.0
   #### expr4 = '~-5!+10'  # יתפרש כ: ~ (5!) + 10 → 5! = 120, ~120 = -120, ואז -120+10 = -110.
    expr5 = '5.5/0'  # לדוגמה, עצרת 5.5 = gamma(6.5)

    print(f"Expression: {expr1} = {calculator.evaluate(expr1)}")
    print(f"Expression: {expr2} = {calculator.evaluate(expr2)}")
    print(f"Expression: {expr3} = {calculator.evaluate(expr3)}")
  ###3  print(f"Expression: {expr4} = {calculator.evaluate(expr4)}")
    print(f"Expression: {expr5} = {calculator.evaluate(expr5)}")

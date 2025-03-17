import unittest

class TestCalculator(unittest.TestCase):
    def setUp(self):
        from chatv3 import Calculator
        self.calc = Calculator()

    def test_basic_operations(self):
        self.assertEqual(self.calc.evaluate('2 + 3'), 5)
        self.assertEqual(self.calc.evaluate('10 - 4'), 6)
        self.assertEqual(self.calc.evaluate('6 * 7'), 42)
        self.assertEqual(self.calc.evaluate('8 / 2'), 4.0)
        self.assertEqual(self.calc.evaluate('4^2*2'), 32)

    def test_order_of_operations(self):
        self.assertEqual(self.calc.evaluate('2 + 3 * 4'), 14)
        self.assertEqual(self.calc.evaluate('(2 + 3!) * 4'), 32)
        self.assertEqual(self.calc.evaluate('100 / (5 + 5)'), 10.0)
        self.assertEqual(self.calc.evaluate('10 - 2 * 3'), 4)

    def test_bitwise_negation_as_negation(self):
        self.assertEqual(self.calc.evaluate('~-5'), 5)  # ~-5 = 5
        self.assertEqual(self.calc.evaluate('~50'), -50)
        self.assertEqual(self.calc.evaluate('~-50'), 50)
        self.assertEqual(self.calc.evaluate('90 + ~-5'), 95)
        self.assertEqual(self.calc.evaluate('7!*(-50 + 95 * 8) - 20 - ~50'), 3578430)
        self.assertEqual(self.calc.evaluate('0!*(10^2*2)'), 200)


    def test_factorial(self):
        self.assertEqual(self.calc.evaluate('5!'), 120)
        self.assertEqual(self.calc.evaluate('0!'), 1)
        self.assertEqual(self.calc.evaluate('1!'), 1)
        #self.assertAlmostEqual(self.calc.evaluate('3.5!'), 11.631)  # עצרת של מספר עשרוני

    def test_complex_expressions(self):
        self.assertEqual(self.calc.evaluate('(5 + 3) * 2!'), 16)
        self.assertEqual(self.calc.evaluate('~-10 + 4!'), 34)  # ~-10 = 10, 10 + 4! = 10 + 24 = 34
        self.assertEqual(self.calc.evaluate('2! + 3! * 4'), 26)

if __name__ == '__main__':
    unittest.main()
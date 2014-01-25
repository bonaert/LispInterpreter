import unittest
from Parse import parse


class ParseTest(unittest.TestCase):
    def test_can_parse_integers(self):
        self.assertEqual(parse('1'), 1)

    def test_can_parse_floats(self):
        self.assertEqual(parse('1.2'), 1.2)

    def test_can_parse_symbols(self):
        self.assertEqual(parse('x'), 'x')

    def test_can_parse_function_call(self):
        self.assertListEqual(parse('(define x 2)'), ['define', 'x', 2])
        self.assertListEqual(parse('(set! x 2)'), ['set!', 'x', 2])

    def test_can_parse_nested_expressions(self):
        self.assertListEqual(parse('(if (= 1 (+ 0 1)) (+ x 1) (car y))'),
                             ['if', ['=', 1, ['+', 0, 1]], ['+', 'x', 1], ['car', 'y']])

    def test_can_parse_begin_statement(self):
        self.assertListEqual(parse('(begin (+ 1 2) y (define x y))'),
                             ['begin', ['+', 1, 2], 'y', ['define', 'x', 'y']])

    def test_can_parse_lambda_expressions(self):
        self.assertListEqual(parse('(lambda x (+ x 2))'), ['lambda', 'x', ['+', 'x', 2]])

    def test_can_parse_call_on_lambda_expression(self):
        code = '((lambda x (+ x 2)) 3)'
        result = [['lambda', 'x', ['+', 'x', 2]], 3]
        self.assertListEqual(parse(code), result)

    def test_can_parse_true_and_false_literals(self):
        code = '(if #f 0 (if #t 1 2))'
        result = ['if', False, 0, ['if', True, 1, 2]]
        self.assertListEqual(parse(code), result)


if __name__ == '__main__':
    unittest.main()
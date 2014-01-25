import unittest
from Parse import parse, InputPort


class ParseTest(unittest.TestCase):
    def assert_parsed_code_equals_result(self):
        parsed_result = parse(InputPort(self.code))

        if isinstance(parsed_result, list):
            self.assertListEqual(parsed_result, self.result)
        else:
            self.assertEqual(parsed_result, self.result)

    def test_can_parse_integers(self):
        self.code = '1'
        self.result = 1
        self.assert_parsed_code_equals_result()

    def test_can_parse_floats(self):
        self.code = '1.2'
        self.result = 1.2
        self.assert_parsed_code_equals_result()

    def test_can_parse_symbols(self):
        self.code = 'x'
        self.result = 'x'
        self.assert_parsed_code_equals_result()

    def test_can_parse_function_call(self):
        self.code = '(define x 2)'
        self.result = ['define', 'x', 2]
        self.assert_parsed_code_equals_result()

        self.code = '(set! x 2)'
        self.result = ['set!', 'x', 2]
        self.assert_parsed_code_equals_result()

    def test_can_parse_nested_expressions(self):
        self.code = '(if (= 1 (+ 0 1)) (+ x 1) (car y))'
        self.result = ['if', ['=', 1, ['+', 0, 1]], ['+', 'x', 1], ['car', 'y']]
        self.assert_parsed_code_equals_result()

    def test_can_parse_begin_statement(self):
        self.code = '(begin (+ 1 2) y (define x y))'
        self.result = ['begin', ['+', 1, 2], 'y', ['define', 'x', 'y']]
        self.assert_parsed_code_equals_result()

    def test_can_parse_lambda_expressions(self):
        self.code = '(lambda x (+ x 2))'
        self.result = ['lambda', 'x', ['+', 'x', 2]]
        self.assert_parsed_code_equals_result()

    def test_can_parse_call_on_lambda_expression(self):
        self.code = '((lambda x (+ x 2)) 3)'
        self.result = [['lambda', 'x', ['+', 'x', 2]], 3]
        self.assert_parsed_code_equals_result()

    def test_can_parse_true_and_false_literals(self):
        self.code = '(if #f 0 (if #t 1 2))'
        self.result = ['if', False, 0, ['if', True, 1, 2]]
        self.assert_parsed_code_equals_result()

    def test_can_parse_string_literals(self):
        self.code = '(if #f "a" (if #t "" "abc123éíóú"))'
        self.result = ['if', False, "a", ['if', True, "", "abc123éíóú"]]
        self.assert_parsed_code_equals_result()

    def test_can_parse_complex_number_literals(self):
        self.code = '(if (+ 1 2j) 2.3 -4.3j )'
        self.result = ['if', ['+', 1, 2j], 2.3, -4.3j]
        self.assert_parsed_code_equals_result()

    def test_can_parse_quotes(self):
        self.code = "'(1 2 3)"
        self.result = ['quote', [1, 2, 3]]
        self.assert_parsed_code_equals_result()

    def test_can_parse_quasi_quotes(self):
        self.code = "`(1 2 3)"
        self.result = ['quasiquote', [1, 2, 3]]
        self.assert_parsed_code_equals_result()


if __name__ == '__main__':
    unittest.main()
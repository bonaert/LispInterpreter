import unittest
import operator
from Eval import eval


class EvalTest(unittest.TestCase):
    def setUp(self):
        self.parsed_code = []
        self.result = ''

    def assert_eval_result_equal(self):
        self.assertEqual(eval(self.parsed_code), self.result)

    def test_can_evaluate_numbers(self):
        self.parsed_code = 1
        self.result = 1
        self.assert_eval_result_equal()

    def test_can_evaluate_if_statements(self):
        self.parsed_code = ['if', False, 0, 1]
        self.result = 1
        self.assert_eval_result_equal()

    def test_can_use_quote(self):
        text = 'I believe I can fly 1 1.2 "Hello" False'
        self.parsed_code = ['quote', text]
        self.result = text
        self.assert_eval_result_equal()

    def test_can_define_things(self):
        self.parsed_code = ['define', 'x', 10]
        self.result = None
        self.assert_eval_result_equal()

    def test_can_define_and_use_things(self):
        self.parsed_code = ['begin', ['define', 'x', 10], 'x']
        self.result = 10
        self.assert_eval_result_equal()

    def test_can_define_and_set_things(self):
        self.parsed_code = ['begin', ['define', 'x', 10], ['set!', 'x', 20], 'x']
        self.result = 20
        self.assert_eval_result_equal()

    def test_can_call_function(self):
        self.parsed_code = [['lambda', ['x'], [operator.add, 'x', 1]], 1]
        self.result = 2
        self.assert_eval_result_equal()

    def test_can_define_and_call_one_var_function(self):
        self.parsed_code = ['begin',
            ['define', 'identity', ['lambda', ['x'], 'x']],
            ['identity', 10]
        ]
        self.result = 10
        self.assert_eval_result_equal()

    def test_can_define_and_call_two_var_function(self):
        self.parsed_code = ['begin',
            ['define', 'mul', ['lambda', ['x', 'y'], [operator.mul, 'x', 'y']]],
            ['mul', 10, 20]
        ]
        self.result = 200
        self.assert_eval_result_equal()


if __name__ == '__main__':
    unittest.main()
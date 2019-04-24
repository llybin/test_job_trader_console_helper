from unittest import TestCase
from unittest.mock import patch, call

from task_1 import calculate, main


class CalculateTest(TestCase):
    def test_ok(self):
        self.assertEqual(
            calculate([
                1.5,
                3,
                6,
                1.5
            ]),
            [
                0.125,
                0.250,
                0.500,
                0.125
            ]
        )

        self.assertEqual(
            calculate([
                1.3,
                1
            ]),
            [
                0.5652173913043479,
                0.4347826086956522,
            ]
        )


class MainTest(TestCase):
    @patch('task_1.ask_share_cnt', return_value=4)
    @patch('task_1.ask_share_value', side_effect=[1.5, 3, 6, 1.5])
    @patch('task_1.print')
    def test_ok(self, mock_print, mock_ask_share_value, mock_ask_share_cnt):
        main()

        self.assertEqual(mock_print.call_count, 4)
        self.assertEqual(
            mock_print.mock_calls,
            list(map(lambda x: call(x), [
                '0.125',
                '0.250',
                '0.500',
                '0.125'
            ]))
        )

    @patch('task_1.ask_share_cnt', return_value=2)
    @patch('task_1.ask_share_value', side_effect=[1.3, 1])
    @patch('task_1.print')
    def test_ok1(self, mock_print, mock_ask_share_value, mock_ask_share_cnt):
        main()

        self.assertEqual(mock_print.call_count, 2)
        self.assertEqual(
            mock_print.mock_calls,
            list(map(lambda x: call(x), [
                '0.565',
                '0.435'
            ]))
        )

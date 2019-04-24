from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch, call

from task_2 import (
    ask_nms_params,
    Params,
    ask_lot_data,
    LotData,
    cost_of_set,
    is_exceeded_lots_per_day,
    profit_of_set,
    calculate,
    main,
)

orig_ask_nms_params = ask_nms_params
orig_ask_lot_data = ask_lot_data


class AskNMSParamsTest(TestCase):
    @patch('task_2.input', return_value='2 2 8000')
    def test_ok(self, mock_input):
        self.assertEqual(
            ask_nms_params(),
            Params(
                day_cnt=2,
                lot_per_day_cnt=2,
                balance=Decimal('8000')
            )
        )
        mock_input.assert_called_with("""Введите через пробел числа, например, 2 2 8000:
            
#1 Близжайщее кол-во дней за которые трейдеру известна информация о том какие предложения по облигациям будут на рынке
#2 Кол-во лотов доступных каждый день
#3 Сумма денежных средст трейдера

:""")

    @patch('task_2.input', return_value='2 2')
    @patch('task_2.ask_nms_params')
    @patch('task_2.print')
    def test_less_data(self, mock_print, mock_ask_nms_params, mock_input):
        orig_ask_nms_params()

        self.assertTrue(mock_ask_nms_params.called)
        self.assertFalse(mock_print.called)

    @patch('task_2.input', return_value='2 2 2 2')
    @patch('task_2.ask_nms_params')
    @patch('task_2.print')
    def test_more_data(self, mock_print, mock_ask_nms_params, mock_input):
        orig_ask_nms_params()

        self.assertTrue(mock_ask_nms_params.called)
        self.assertFalse(mock_print.called)

    @patch('task_2.input', return_value='-2 2 2')
    @patch('task_2.ask_nms_params')
    @patch('task_2.print')
    def test_day_negative(self, mock_print, mock_ask_nms_params, mock_input):
        orig_ask_nms_params()

        self.assertTrue(mock_ask_nms_params.called)
        mock_print.assert_called_with("\n!!!\nКол-во дней не может быть отрицательным\n!!!\n")

    @patch('task_2.input', return_value='2.2 2 2')
    @patch('task_2.ask_nms_params')
    @patch('task_2.print')
    def test_day_not_int(self, mock_print, mock_ask_nms_params, mock_input):
        orig_ask_nms_params()

        self.assertTrue(mock_ask_nms_params.called)
        mock_print.assert_called_with("\n!!!\nКол-во дней должно быть целым числом\n!!!\n")

    @patch('task_2.input', return_value='a 2 2')
    @patch('task_2.ask_nms_params')
    @patch('task_2.print')
    def test_day_not_int(self, mock_print, mock_ask_nms_params, mock_input):
        orig_ask_nms_params()

        self.assertTrue(mock_ask_nms_params.called)
        mock_print.assert_called_with("\n!!!\nКол-во дней должно быть целым числом\n!!!\n")

    @patch('task_2.input', return_value='0 2 2')
    def test_day_zero(self, mock_input):
        self.assertEqual(
            ask_nms_params(),
            Params(
                day_cnt=0,
                lot_per_day_cnt=2,
                balance=Decimal('2')
            )
        )

    @patch('task_2.input', return_value='2 -1 2')
    @patch('task_2.ask_nms_params')
    @patch('task_2.print')
    def test_lot_cnt_negative(self, mock_print, mock_ask_nms_params, mock_input):
        orig_ask_nms_params()

        self.assertTrue(mock_ask_nms_params.called)
        mock_print.assert_called_with("\n!!!\nКол-во лотов в день не может быть отрицательным\n!!!\n")

    @patch('task_2.input', return_value='2 a 2')
    @patch('task_2.ask_nms_params')
    @patch('task_2.print')
    def test_lot_cnt_string(self, mock_print, mock_ask_nms_params, mock_input):
        orig_ask_nms_params()

        self.assertTrue(mock_ask_nms_params.called)
        mock_print.assert_called_with("\n!!!\nКол-во лотов должно быть целым числом\n!!!\n")

    @patch('task_2.input', return_value='2 2.2 2')
    @patch('task_2.ask_nms_params')
    @patch('task_2.print')
    def test_lot_cnt_not_int(self, mock_print, mock_ask_nms_params, mock_input):
        orig_ask_nms_params()

        self.assertTrue(mock_ask_nms_params.called)
        mock_print.assert_called_with("\n!!!\nКол-во лотов должно быть целым числом\n!!!\n")

    @patch('task_2.input', return_value='2 0 2')
    def test_lot_cnt_zero(self, mock_input):
        self.assertEqual(
            ask_nms_params(),
            Params(
                day_cnt=2,
                lot_per_day_cnt=0,
                balance=Decimal('2')
            )
        )

    @patch('task_2.input', return_value='2 2 -1')
    @patch('task_2.ask_nms_params')
    @patch('task_2.print')
    def test_balance_negative(self, mock_print, mock_ask_nms_params, mock_input):
        orig_ask_nms_params()

        self.assertTrue(mock_ask_nms_params.called)
        mock_print.assert_called_with("\n!!!\nБаланс не может быть отрицательным или неопределеным\n!!!\n")

    @patch('task_2.input', return_value='2 2 inf')
    @patch('task_2.ask_nms_params')
    @patch('task_2.print')
    def test_balance_inf(self, mock_print, mock_ask_nms_params, mock_input):
        orig_ask_nms_params()

        self.assertTrue(mock_ask_nms_params.called)
        mock_print.assert_called_with("\n!!!\nБаланс не может быть отрицательным или неопределеным\n!!!\n")

    @patch('task_2.input', return_value='2 2 a')
    @patch('task_2.ask_nms_params')
    @patch('task_2.print')
    def test_balance_not_digits(self, mock_print, mock_ask_nms_params, mock_input):
        orig_ask_nms_params()

        self.assertTrue(mock_ask_nms_params.called)
        mock_print.assert_called_with("\n!!!\nБаланс должен быть числом\n!!!\n")

    @patch('task_2.input', return_value='2 2 0')
    def test_balance_zero(self, mock_input):
        self.assertEqual(
            ask_nms_params(),
            Params(
                day_cnt=2,
                lot_per_day_cnt=2,
                balance=Decimal('0')
            )
        )


class AskLotDataTest(TestCase):
    @patch('task_2.input', return_value='1 alfa-05 100.2 2')
    def test_ok(self, mock_input):
        self.assertEqual(
            ask_lot_data(),
            LotData(
                day=1,
                name='alfa-05',
                price=Decimal('100.2'),
                cnt=2
            )
        )
        mock_input.assert_called_with("""Введите <день> <название облигации в виде строки без пробелов> <цена> <количество>
Чтобы закончить ввод данных нажмите Enter не заполняя поле
:""")

    @patch('task_2.input', return_value='1 alfa-05 100.2')
    @patch('task_2.ask_lot_data')
    @patch('task_2.print')
    def test_less_data(self, mock_print, mock_ask_lot_data, mock_input):
        orig_ask_lot_data()

        self.assertTrue(mock_ask_lot_data.called)
        self.assertFalse(mock_print.called)

    @patch('task_2.input', return_value='1 alfa-05 100.2 2 2')
    @patch('task_2.ask_lot_data')
    @patch('task_2.print')
    def test_more_data(self, mock_print, mock_ask_lot_data, mock_input):
        orig_ask_lot_data()

        self.assertTrue(mock_ask_lot_data.called)
        self.assertFalse(mock_print.called)

    @patch('task_2.input', return_value='')
    def test_exit(self, mock_input):
        self.assertEqual(
            ask_lot_data(),
            None
        )

    @patch('task_2.input', return_value=' ')
    @patch('task_2.ask_lot_data')
    @patch('task_2.print')
    def test_empty_string(self, mock_print, mock_ask_lot_data, mock_input):
        orig_ask_lot_data()

        self.assertTrue(mock_ask_lot_data.called)
        self.assertFalse(mock_print.called)

    @patch('task_2.input', return_value='0 alfa-05 100.2 2')
    @patch('task_2.ask_lot_data')
    @patch('task_2.print')
    def test_day_zero(self, mock_print, mock_ask_lot_data, mock_input):
        orig_ask_lot_data()

        self.assertTrue(mock_ask_lot_data.called)
        mock_print.assert_called_with("\n!!!\nДень должен быть положительным числом\n!!!\n")

    @patch('task_2.input', return_value='-1 alfa-05 100.2 2')
    @patch('task_2.ask_lot_data')
    @patch('task_2.print')
    def test_day_negative(self, mock_print, mock_ask_lot_data, mock_input):
        orig_ask_lot_data()

        self.assertTrue(mock_ask_lot_data.called)
        mock_print.assert_called_with("\n!!!\nДень должен быть положительным числом\n!!!\n")

    @patch('task_2.input', return_value='1.1 alfa-05 100.2 2')
    @patch('task_2.ask_lot_data')
    @patch('task_2.print')
    def test_day_not_int(self, mock_print, mock_ask_lot_data, mock_input):
        orig_ask_lot_data()

        self.assertTrue(mock_ask_lot_data.called)
        mock_print.assert_called_with("\n!!!\nДень должен быть целым числом\n!!!\n")

    @patch('task_2.input', return_value='a alfa-05 100.2 2')
    @patch('task_2.ask_lot_data')
    @patch('task_2.print')
    def test_day_string(self, mock_print, mock_ask_lot_data, mock_input):
        orig_ask_lot_data()

        self.assertTrue(mock_ask_lot_data.called)
        mock_print.assert_called_with("\n!!!\nДень должен быть целым числом\n!!!\n")

    @patch('task_2.input', return_value='1 alfa-05 0 2')
    @patch('task_2.ask_lot_data')
    @patch('task_2.print')
    def test_price_zero(self, mock_print, mock_ask_lot_data, mock_input):
        orig_ask_lot_data()

        self.assertTrue(mock_ask_lot_data.called)
        mock_print.assert_called_with("\n!!!\nЦена должна быть положительной\n!!!\n")

    @patch('task_2.input', return_value='1 alfa-05 -1 2')
    @patch('task_2.ask_lot_data')
    @patch('task_2.print')
    def test_price_negative(self, mock_print, mock_ask_lot_data, mock_input):
        orig_ask_lot_data()

        self.assertTrue(mock_ask_lot_data.called)
        mock_print.assert_called_with("\n!!!\nЦена должна быть положительной\n!!!\n")

    @patch('task_2.input', return_value='1 alfa-05 inf 2')
    @patch('task_2.ask_lot_data')
    @patch('task_2.print')
    def test_price_inf(self, mock_print, mock_ask_lot_data, mock_input):
        orig_ask_lot_data()

        self.assertTrue(mock_ask_lot_data.called)
        mock_print.assert_called_with("\n!!!\nЦена должна быть положительной\n!!!\n")

    @patch('task_2.input', return_value='1 alfa-05 100.2 2')
    def test_price_float(self, mock_input):
        self.assertEqual(
            ask_lot_data(),
            LotData(
                day=1,
                name='alfa-05',
                price=Decimal('100.2'),
                cnt=2
            )
        )

    @patch('task_2.input', return_value='1 alfa-05 a 2')
    @patch('task_2.ask_lot_data')
    @patch('task_2.print')
    def test_price_string(self, mock_print, mock_ask_lot_data, mock_input):
        orig_ask_lot_data()

        self.assertTrue(mock_ask_lot_data.called)
        mock_print.assert_called_with("\n!!!\nЦена должна быть числом\n!!!\n")

    @patch('task_2.input', return_value='1 alfa-05 100.2 0')
    def test_bond_cnt_zero(self, mock_input):
        self.assertEqual(
            ask_lot_data(),
            LotData(
                day=1,
                name='alfa-05',
                price=Decimal('100.2'),
                cnt=0
            )
        )

    @patch('task_2.input', return_value='1 alfa-05 100.2 -1')
    @patch('task_2.ask_lot_data')
    @patch('task_2.print')
    def test_bond_cnt_negative(self, mock_print, mock_ask_lot_data, mock_input):
        orig_ask_lot_data()

        self.assertTrue(mock_ask_lot_data.called)
        mock_print.assert_called_with("\n!!!\nКол-во не может быть отрицательным\n!!!\n")

    @patch('task_2.input', return_value='1 alfa-05 100.2 1.1')
    @patch('task_2.ask_lot_data')
    @patch('task_2.print')
    def test_bond_cnt_not_int(self, mock_print, mock_ask_lot_data, mock_input):
        orig_ask_lot_data()

        self.assertTrue(mock_ask_lot_data.called)
        mock_print.assert_called_with("\n!!!\nКол-во должно быть целым числом\n!!!\n")

    @patch('task_2.input', return_value='1 alfa-05 100.2 a')
    @patch('task_2.ask_lot_data')
    @patch('task_2.print')
    def test_bond_cnt_string(self, mock_print, mock_ask_lot_data, mock_input):
        orig_ask_lot_data()

        self.assertTrue(mock_ask_lot_data.called)
        mock_print.assert_called_with("\n!!!\nКол-во должно быть целым числом\n!!!\n")


class CostOfSetTest(TestCase):
    def test_empty(self):
        self.assertEqual(cost_of_set([]), 0)

    def test_zero_price(self):
        self.assertEqual(cost_of_set([
            LotData(1, 'test', Decimal('0'), 2)
        ]), Decimal('0'))

    def test_zero_count(self):
        self.assertEqual(cost_of_set([
            LotData(1, 'test', Decimal('10.13'), 0)
        ]), Decimal('0'))

    def test_ok(self):
        self.assertEqual(cost_of_set([
            LotData(1, 'test', Decimal('10'), 1)
        ]), Decimal('100'))

        self.assertEqual(cost_of_set([
            LotData(1, 'test', Decimal('10.13'), 2)
        ]), Decimal('202.6'))

        self.assertEqual(cost_of_set([
            LotData(1, 'test', Decimal('10.13'), 2),
            LotData(1, 'test', Decimal('10.33'), 3),
        ]), Decimal('512.5'))


class IsExceededLotsPerDayTest(TestCase):
    def test_false(self):
        self.assertFalse(
            is_exceeded_lots_per_day([
                LotData(1, 'test', Decimal('10.13'), 2),
                LotData(1, 'test', Decimal('10.33'), 3),
            ], Params(day_cnt=2, lot_per_day_cnt=2, balance=Decimal('8000'))))

        self.assertFalse(
            is_exceeded_lots_per_day([
                LotData(1, 'test', Decimal('10.13'), 2),
                LotData(1, 'test', Decimal('10.33'), 3),
                LotData(1, 'test', Decimal('10.33'), 3),
            ], Params(day_cnt=2, lot_per_day_cnt=3, balance=Decimal('8000'))))

    def test_true(self):
        self.assertTrue(
            is_exceeded_lots_per_day([
                LotData(1, 'test', Decimal('10.13'), 2),
                LotData(1, 'test', Decimal('10.33'), 3),
                LotData(1, 'test', Decimal('10.33'), 3),
            ], Params(day_cnt=2, lot_per_day_cnt=2, balance=Decimal('8000'))))

    def test_zero_true(self):
        self.assertTrue(
            is_exceeded_lots_per_day([
                LotData(1, 'test', Decimal('10.13'), 2),
                LotData(1, 'test', Decimal('10.33'), 3),
                LotData(1, 'test', Decimal('10.33'), 3),
            ], Params(day_cnt=2, lot_per_day_cnt=0, balance=Decimal('8000'))))

    def test_empty(self):
        self.assertFalse(
            is_exceeded_lots_per_day([], Params(day_cnt=2, lot_per_day_cnt=0, balance=Decimal('8000'))))


class ProfitOfSetTest(TestCase):
    def test_ok(self):
        self.assertEqual(
            profit_of_set([
                LotData(day=2, name='alfa-05', price=Decimal('101.5'), cnt=5),
                LotData(day=2, name='gazprom-17', price=Decimal('100.0'), cnt=2),
            ], Params(day_cnt=2, lot_per_day_cnt=2, balance=Decimal('8000'))),
            Decimal('135'))

        self.assertEqual(
            profit_of_set([
                LotData(day=1, name='alfa-05', price=Decimal('101.5'), cnt=5),
                LotData(day=2, name='gazprom-17', price=Decimal('100.0'), cnt=2),
            ], Params(day_cnt=2, lot_per_day_cnt=2, balance=Decimal('8000'))),
            Decimal('140'))

    def test_empty(self):
        self.assertEqual(
            profit_of_set([], Params(day_cnt=2, lot_per_day_cnt=2, balance=Decimal('8000'))),
            Decimal('0'))

    def test_zero_price(self):
        self.assertEqual(
            profit_of_set([
                LotData(day=2, name='alfa-05', price=Decimal('0'), cnt=1),
            ], Params(day_cnt=2, lot_per_day_cnt=2, balance=Decimal('8000'))),
            Decimal('1030'))

        self.assertEqual(
            profit_of_set([
                LotData(day=1, name='alfa-05', price=Decimal('0'), cnt=1),
            ], Params(day_cnt=2, lot_per_day_cnt=2, balance=Decimal('8000'))),
            Decimal('1031'))

    def test_zero_count(self):
        self.assertEqual(
            profit_of_set([
                LotData(day=2, name='alfa-05', price=Decimal('10.13'), cnt=0),
            ], Params(day_cnt=2, lot_per_day_cnt=2, balance=Decimal('8000'))),
            Decimal('0'))


class CalculateTest(TestCase):
    def test_ok(self):
        self.assertEqual(
            calculate([
                LotData(day=1, name='alfa-05', price=Decimal('100.2'), cnt=2),
                LotData(day=2, name='alfa-05', price=Decimal('101.5'), cnt=5),
                LotData(day=2, name='gazprom-17', price=Decimal('100.0'), cnt=2),
            ], Params(day_cnt=2, lot_per_day_cnt=2, balance=Decimal('8000'))),
            (Decimal('135'), (
                LotData(day=2, name='alfa-05', price=Decimal('101.5'), cnt=5),
                LotData(day=2, name='gazprom-17', price=Decimal('100.0'), cnt=2),
            )))

        self.assertEqual(
            calculate([
                LotData(day=1, name='alfa-05', price=Decimal('100.2'), cnt=2),
                LotData(day=2, name='alfa-05', price=Decimal('101.5'), cnt=5),
                LotData(day=2, name='gazprom-17', price=Decimal('100.0'), cnt=2),
                LotData(day=2, name='gazprom-18', price=Decimal('110.0'), cnt=1),
            ], Params(day_cnt=2, lot_per_day_cnt=2, balance=Decimal('8000'))),
            (Decimal('135'), (
                LotData(day=2, name='alfa-05', price=Decimal('101.5'), cnt=5),
                LotData(day=2, name='gazprom-17', price=Decimal('100.0'), cnt=2),
            )))

    def test_3_best_in_1_day(self):
        self.assertEqual(
            calculate([
                LotData(day=1, name='alfa-04', price=Decimal('100'), cnt=1),
                LotData(day=1, name='alfa-05', price=Decimal('100'), cnt=1),
                LotData(day=1, name='alfa-06', price=Decimal('100'), cnt=1),
                LotData(day=1, name='alfa-07', price=Decimal('102'), cnt=1),
                LotData(day=2, name='gaz-04', price=Decimal('100'), cnt=1),
                LotData(day=2, name='gaz-05', price=Decimal('100'), cnt=1),
                LotData(day=2, name='gaz-06', price=Decimal('101'), cnt=1),
            ], Params(day_cnt=2, lot_per_day_cnt=2, balance=Decimal('8000'))),
            (Decimal('122'), (
                LotData(day=1, name='alfa-04', price=Decimal('100'), cnt=1),
                LotData(day=1, name='alfa-05', price=Decimal('100'), cnt=1),
                LotData(day=2, name='gaz-04', price=Decimal('100'), cnt=1),
                LotData(day=2, name='gaz-05', price=Decimal('100'), cnt=1)
            )))

    def test_balance(self):
        self.assertEqual(
            calculate([
                LotData(day=1, name='alfa-04', price=Decimal('100'), cnt=1),
                LotData(day=1, name='alfa-05', price=Decimal('100'), cnt=1),
                LotData(day=1, name='alfa-06', price=Decimal('100'), cnt=1),
                LotData(day=1, name='alfa-07', price=Decimal('102'), cnt=1),
                LotData(day=2, name='gaz-04', price=Decimal('99'), cnt=1),
                LotData(day=2, name='gaz-05', price=Decimal('100'), cnt=1),
                LotData(day=2, name='gaz-06', price=Decimal('101'), cnt=1),
            ], Params(day_cnt=2, lot_per_day_cnt=2, balance=Decimal('1000'))),
            (Decimal('40'), (
                LotData(day=2, name='gaz-04', price=Decimal('99'), cnt=1),
            )))


class MainTest(TestCase):
    @patch('task_2.ask_nms_params', return_value=Params(
        day_cnt=2,
        lot_per_day_cnt=2,
        balance=Decimal('8000')
    ))
    @patch('task_2.ask_lot_data', side_effect=[
        LotData(
            day=1,
            name='alfa-05',
            price=Decimal('100.2'),
            cnt=2
        ),
        LotData(
            day=2,
            name='alfa-05',
            price=Decimal('101.5'),
            cnt=5
        ),
        LotData(
            day=2,
            name='gazprom-17',
            price=Decimal('100.0'),
            cnt=2
        ),
        None
    ])
    @patch('task_2.print')
    def test_ok(self, mock_print, mock_ask_lot_data, mock_ask_nms_params):
        main()

        self.assertEqual(mock_print.call_count, 7)
        self.assertEqual(
            mock_print.mock_calls,
            list(map(lambda x: call(x), [
                '\nДобавлено!\n',
                '\nДобавлено!\n',
                '\nДобавлено!\n',
                Decimal('135.000'),
                '2 alfa-05 101.5 5',
                '2 gazprom-17 100.0 2',
                ''
            ])))

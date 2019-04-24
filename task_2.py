import collections
import decimal
import itertools
import math
from typing import NamedTuple


class ValidateError(Exception):
    pass


def validate_day_cnt(value):
    try:
        value = int(value)
    except ValueError:
        raise ValidateError("Кол-во дней должно быть целым числом")

    if value < 0:
        raise ValidateError("Кол-во дней не может быть отрицательным")

    return value


def validate_lot_per_day_cnt(value):
    try:
        value = int(value)
    except ValueError:
        raise ValidateError("Кол-во лотов должно быть целым числом")

    if value < 0:
        raise ValidateError("Кол-во лотов в день не может быть отрицательным")

    return value


def validate_balance(value):
    try:
        value = decimal.Decimal(value)
    except decimal.DecimalException:
        raise ValidateError("Баланс должен быть числом")

    if value < 0 or math.isinf(value):
        raise ValidateError("Баланс не может быть отрицательным или неопределеным")

    return value


class Params(NamedTuple):
    day_cnt: int
    lot_per_day_cnt: int
    balance: decimal.Decimal


def ask_nms_params():
    # while True:
    try:
        nms_params = input(
            """Введите через пробел числа, например, 2 2 8000:
            
#1 Близжайщее кол-во дней за которые трейдеру известна информация о том какие предложения по облигациям будут на рынке
#2 Кол-во лотов доступных каждый день
#3 Сумма денежных средст трейдера

:""")

        day_cnt, lot_per_day_cnt, balance = nms_params.split()

        day_cnt = validate_day_cnt(day_cnt)
        lot_per_day_cnt = validate_lot_per_day_cnt(lot_per_day_cnt)
        balance = validate_balance(balance)

        return Params(day_cnt, lot_per_day_cnt, balance)

    except ValueError:
        return ask_nms_params()

    except ValidateError as e:
        print(f"\n!!!\n{e}\n!!!\n")
        return ask_nms_params()


def validate_day(value):
    try:
        value = int(value)
    except ValueError:
        raise ValidateError("День должен быть целым числом")

    if value <= 0:
        raise ValidateError("День должен быть положительным числом")

    return value


def validate_price(value):
    try:
        value = decimal.Decimal(value)
    except decimal.DecimalException:
        raise ValidateError("Цена должна быть числом")

    if value <= 0 or math.isinf(value):
        raise ValidateError("Цена должна быть положительной")

    return value


def validate_bond_cnt(value):
    try:
        value = int(value)
    except ValueError:
        raise ValidateError("Кол-во должно быть целым числом")

    if value < 0:
        raise ValidateError("Кол-во не может быть отрицательным")

    return value


class LotData(NamedTuple):
    day: int
    name: str
    price: decimal.Decimal
    cnt: int


def ask_lot_data():
    try:
        data = input("""Введите <день> <название облигации в виде строки без пробелов> <цена> <количество>
Чтобы закончить ввод данных нажмите Enter не заполняя поле
:""")

        if len(data) == 0:
            return None

        day, name, price, cnt = data.split()

        day = validate_day(day)
        price = validate_price(price)
        cnt = validate_bond_cnt(cnt)

        return LotData(day, name, price, cnt)

    except ValueError:
        return ask_lot_data()

    except ValidateError as e:
        print(f"\n!!!\n{e}\n!!!\n")
        return ask_lot_data()


def cost_of_set(set_lots):
    return sum(map(
        lambda l: l.price / 100 * 1000 * l.cnt,
        set_lots))


def is_exceeded_lots_per_day(set_lots, params):
    day_counter = collections.Counter(map(lambda x: x.day, set_lots))

    return any(filter(
        lambda x: x[1] > params.lot_per_day_cnt,
        day_counter.items()))


def profit_of_set(set_lots, params):
    return sum(map(
        lambda l: (1000 - l.price / 100 * 1000 + (30 + params.day_cnt - l.day)) * l.cnt,
        set_lots))


def calculate(lots, params):
    best_profit = 0
    best_set = set()

    for l in range(0, len(lots) + 1):
        for set_lots in itertools.combinations(lots, l):
            needed_balance = cost_of_set(set_lots)
            is_exceeded_days = is_exceeded_lots_per_day(set_lots, params)

            if needed_balance <= params.balance and not is_exceeded_days:
                profit = profit_of_set(set_lots, params)

                if best_profit < profit:
                    best_profit = profit
                    best_set = set_lots

    return best_profit, best_set


def main():
    nms_params = ask_nms_params()

    lots = []

    while True:
        lot_data = ask_lot_data()

        if not lot_data:
            break

        print("\nДобавлено!\n")

        lots.append(lot_data)

    best_profit, best_set = calculate(lots, nms_params)

    print(best_profit)

    for x in best_set:
        print(f"{x.day} {x.name} {x.price} {x.cnt}")

    print('')


if __name__ == "__main__":
    main()

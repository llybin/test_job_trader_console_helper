import math


def ask_share_cnt():
    while True:
        try:
            share_cnt = int(input("Введите кол-во долей: "))

            if share_cnt <= 0:
                raise ValueError

        except ValueError:
            print("Пожалуйста, введите целое положительное число!")

        else:
            return share_cnt


def ask_share_value(number):
    while True:
        try:
            share_value = float(input(f"Введите долю #{number}: "))

            if share_value <= 0 or math.isinf(share_value):
                raise ValueError

        except ValueError:
            print("Пожалуйста, введите положительное число!")

        else:
            return share_value


def calculate(shares):
    shares_in_perc = []

    shares_sum = sum(shares)

    for share in shares:
        shares_in_perc.append(share / shares_sum)

    return shares_in_perc


def main():
    share_cnt = ask_share_cnt()
    shares = []

    for n in range(1, share_cnt + 1):
        shares.append(ask_share_value(n))

    shares_in_perc = calculate(shares)

    for s in shares_in_perc:
        print(f"{s:.3f}")


if __name__ == "__main__":
    main()

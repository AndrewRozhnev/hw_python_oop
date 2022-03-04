from typing import Optional
import datetime as dt


class Record:
    """Создание записей."""

    def __init__(self, amount: float, comment: str, date: Optional[str] = None) -> None:
        """
        :param amount: Денежная сумма или количество килокалорий.
        :param comment: Комментарий, поясняющий, на что потрачены деньги или откуда взялись калории.
        :param date: Дата создания записи. Формат даты для получения: '%d.%m.%Y'
        """
        self.amount = amount
        self.comment = comment

        if date is None:
            # Задаём текущую дату в формате объекта datetime
            self.date = dt.date.today()
        else:
            # или переводим переданную строку в объект класса datetime
            str_to_datetime = dt.datetime.strptime(date, '%d.%m.%Y').date()
            self.date = str_to_datetime


class Calculator:
    """Родительский класс для обоих калькуляторов."""

    def __init__(self, limit: float) -> None:
        """:param limit: Дневной лимит трат/калорий, который задал пользователь."""
        self.limit = limit
        # Список для хранения каких-либо записей (о еде или деньгах)
        self.records = []

    def add_record(self, new_record: Record) -> None:
        """Сохраняем новую запись о расходах/приёме пищи."""
        self.records.append(new_record)

    def get_today_stats(self) -> float:
        """Считаем, сколько денег/(калорий) потрачено/(съедено) сегодня."""
        return sum([record.amount
                    for record in self.records
                    if record.date == dt.date.today()])

    def get_week_stats(self) -> float:
        """Считаем, сколько денег/(калорий) потрачено/(получено) за последние 7 дней."""
        date_week_ago = dt.date.today() - dt.timedelta(days=7)
        return sum([record.amount
                    for record in self.records
                    if date_week_ago <= record.date <= dt.date.today()])

    def get_today_remained(self) -> float:
        """Считаем, сколько денег/(калорий) можно ещё сегодня потратить/(съесть)."""
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    """Калькулятор для подсчёта калорий"""

    def get_calories_remained(self) -> str:
        """Определяем, сколько ещё калорий можно/нужно получить сегодня."""
        if self.get_today_remained() > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {self.get_today_remained()} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    """Калькулятор для подсчёта денег."""

    # Курсы валют
    RUB_RATE = 1.0
    USD_RATE = 60.56
    EURO_RATE = 75.89

    def get_today_cash_remained(self, currency: str = 'rub') -> str:
        """Определяем, сколько ещё денег можно потратить сегодня в рублях, долларах или евро.
        :param currency: Код валюты, 'rub', 'usd' или 'eur'.
        """

        all_currency = {
            'rub': ('руб', self.RUB_RATE),
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE)
        }

        currency_name, currency_rate = all_currency[currency]
        today_remained_abs = round(abs(self.get_today_remained() / currency_rate), 2)

        if self.get_today_remained() == 0:
            return 'Денег нет, держись'
        if self.get_today_remained() > 0:
            return f'На сегодня осталось {today_remained_abs} {currency_name}'
        else:
            # Если мы залезли в долги, то get_today_remained вернёт отрицательное число
            # это и будет наш долг (нам нужен модуль этого числа - abs)
            return f'Денег нет, держись: твой долг - {today_remained_abs} {currency_name}'


if __name__ == '__main__':
    pass

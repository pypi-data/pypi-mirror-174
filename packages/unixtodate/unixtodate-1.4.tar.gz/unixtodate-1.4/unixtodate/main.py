from datetime import date, datetime

class ToDate:
    def __init__(self, timestamp: int, lang='ru'):
        """
        :param timestamp: время в unix timestamp в прошлом
        :param lang: 'ru' или 'en'
        """
        self.timestamp = timestamp
        self.lang = lang if lang in ['ru', 'en'] else 'ru'

    def get_count_days(self):
        """
        Узнать количество дней прошедших с указанной timestamp даты
        :return:
        """
        today = date.today()
        fromtimestamp = datetime.fromtimestamp(self.timestamp).date()

        s = str(today - fromtimestamp).split()[0]
        s = int(s) if s != '0:00:00' else 0
        return s

    def get_day_word(self, lang=None):
        """
        Получить слово "день" с нужным окончанием
        :param lang: 'ru' или 'en'
        :return: слово "день" на заданном языке с нужным окончанием в соответствии с количеством прошедших дней
        """
        if lang is None:
            lang = self.lang

        s = self.get_count_days()
        s = s if s > 0 else s*-1

        if lang == 'ru':
            if (s == 0) or (s % 100 >= 10 and s % 100 <= 20):
                return 'дней'
            elif s % 10 == 1:
                return 'день'
            elif s % 10 >= 2 and s % 10 <= 4:
                return 'дня'
            else:
                return 'дней'

        elif lang == 'en':
            return 'day' if s == 1 else 'days'

    def get_days_and_word(self, lang=None):
        return f'{self.get_count_days()} {self.get_day_word(lang)}'
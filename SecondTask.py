import datetime
from datetime import date, timedelta
import requests
import psycopg2
from colorama import Fore


class Note:
    check_number = 0

    def __init__(self, current_date, current_time, first_currency, second_currency, rate, color):
        self.current_date = current_date
        self.current_time = current_time
        self.first_currency = first_currency
        self.second_currency = second_currency
        self.rate = rate
        self.color = color

    def get_api_key(self, file):
        with open(file, 'r') as file:
            api = file.read().splitlines()
            api_key = ''.join(api)
            return str(api_key)

    def change_currency(self):

        today = date.today()
        today_date = datetime.datetime.now()
        today_time = today_date.strftime("%H:%M:%S")
        yesterday = str(today - timedelta(days=1))
        database_value = 1

        print('Enter two currencies with whitespace between them.\nFor closing type "quit", for history view type '
              '"history"')

        while True:

            users_input = input(Fore.RESET).lower()

            if users_input == 'quit':
                print('Closing the the app.')
                exit(1)
            elif users_input == 'history':
                print('Printing out the history:')
                Note.print_out_database(self)
                print('\n')
                Note.check_number += 1
                Note.change_currency(self)

            users_input = users_input.upper()
            currency_input = users_input.split()
            currencies = '_'.join(currency_input)

            api_key = Note.get_api_key(self, 'api_key.txt')

            actual_rate_path = ('https://free.currconv.com/api/v7/convert?q=' + currencies + '&compact=ultra&apiKey'
                                + api_key)
            exchange_rate = requests.get(actual_rate_path).json()

            if currencies not in exchange_rate:
                print('Wrong input\n')
                Note.check_number += 1
                Note.change_currency(self)

            yesterday_path = 'https://free.currconv.com/api/v7/convert?q=' + currencies + '&compact=ultra&date=' \
                             + yesterday + '&apiKey' + api_key
            yesterday_rate = requests.get(yesterday_path).json()
            yesterday_value = float()

            first_currency = currency_input[0]
            second_currency = currency_input[1]

            for value in yesterday_rate.values():
                for specific_value in value.values():
                    yesterday_value = specific_value

            if currencies in actual_rate_path:
                for value in exchange_rate.values():
                    if value > yesterday_value:
                        value = '{:.2f}'.format(value)
                        print(Fore.GREEN + value)
                        color = 'GREEN'
                        row = Note(today, today_time, first_currency, second_currency, value, color)
                        Note.insert_into_database(self, row.current_date, row.current_time, row.first_currency,
                                                  row.second_currency, row.rate, database_value, color)
                        database_value += 1

                    elif value < yesterday_value:
                        value = '{:.2f}'.format(value)
                        print(Fore.RED + value)
                        color = 'RED'
                        row = Note(today, today_time, first_currency, second_currency, value, color)
                        Note.insert_into_database(self, row.current_date, row.current_time, row.first_currency,
                                                  row.second_currency, row.rate, database_value, color)
                        database_value += 1

    def insert_into_database(self, today_date, today_time, from_currency, to_currency, exchange_rate, database_value,
                             color):

        connection = psycopg2.connect(user='postgres', password='postgres', database='postgres', host='localhost')
        connection.autocommit = True
        cursor = connection.cursor()

        if database_value == 1 and Note.check_number == 0:
            cursor.execute('CREATE TABLE Exchange_Currency(today_date text, today_time text, from_currency text, '
                           'to_currency text, exchange_rate text, color text)')

        command = '''INSERT INTO Exchange_Currency(today_date, today_time, from_currency, to_currency, exchange_rate, 
                            color) VALUES(%s,%s,%s,%s,%s,%s) '''
        cursor.execute(command, (today_date, today_time, from_currency, to_currency, exchange_rate, color))
        connection.commit()
        connection.close()

    def print_out_database(self):
        connection = psycopg2.connect(user='postgres', password='postgres', database='postgres', host='localhost')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Exchange_Currency')
        rows = cursor.fetchall()
        for row in rows:
            if row[-1] == 'GREEN':
                print(Fore.GREEN + str(row[0:5]), Fore.RESET)
            elif row[-1] == 'RED':
                print(Fore.RED + str(row[0:5]), Fore.RESET)


Note.change_currency('')

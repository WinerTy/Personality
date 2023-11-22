import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.set_button()
        self.currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CNY','KZT','UAH','AED']
        self.metal = ['Золото','Серебро','Платина','Палладий']
        self.stocks = ['AAPL','MSFT','AMZN']
        self.answer_info = ['Актуальная стоимость валюты берется с офицального сайта Банка России:\nhttps://cbr.ru/currency_base/daily/', 'Актуальная стоимость Металлов берется с офицального сайта Банка России:\nhttps://cbr.ru/hd_base/metall/metall_base_new/', 'Актуальная стоимость акций берется с сайта finnhub и обновляются в реальном времени:\nhttps://finnhub.io/', 'Все реализуемые запросы выполняются двумя методами:\n Первый метод происходит через анализ веб страницы, данный метод используется для Валюты и Металлов(Нужно больше времени на обработку запроса).\nВторой реализован через запрос к API и обновляется в реальном времени(Происходит быстрее чем первый). ']
        self.API_KEY = 'clf1ddpr01qovepph9dgclf1ddpr01qovepph9e0'
        # Блок КНОПОК
    def set_button(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            item1 = types.KeyboardButton('💹Курс валют💹')  # Название кнопки
            item2 = types.KeyboardButton('💎Курс металлов💎')  # Название кнопки
            item3 = types.KeyboardButton('📈Цена акций📈')  # Название кнопки
            item4 = types.KeyboardButton('❓Информация❓')  # Название кнопки
            markup.row(item4)
            markup.row(item1, item2, item3)
            self.bot.send_message(message.chat.id,'Вы в главном меню',reply_markup=markup)


        # БЛОК ЛОГИКИ
        @self.bot.message_handler(content_types=['text'])
        def handle_text(message):
            if message.text == '💹Курс валют💹':
                self.show_currency_menu(message)

            elif message.text == '💎Курс металлов💎':
                self.show_metal_menu(message)

            elif message.text == '📈Цена акций📈':
                self.show_stock_menu(message)

            elif message.text == '❓Информация❓':
                self.show_info(message)

            elif message.text == 'Пункт 1':
                self.bot.send_message(message.chat.id, self.answer_info[0])

            elif message.text == 'Пункт 2':
                self.bot.send_message(message.chat.id, self.answer_info[1])

            elif message.text == 'Пункт 3':
                self.bot.send_message(message.chat.id, self.answer_info[2])

            elif message.text == 'Пункт 4':
                self.bot.send_message(message.chat.id, self.answer_info[3])

            elif message.text in self.currencies:
                self.show_value_info(message, message.text)
                self.get_currency_info(message)


            elif message.text in self.metal:
                self.show_metal_info(message, message.text)
                self.get_metal_info(message)

            elif message.text in self.stocks:
                self.show_stock_info(message, message.text)
                self.get_stock_info(message)

            elif message.text == 'Меню':
                start(message)

    # БЛОК ВАЛЮТЫ
    def show_currency_menu(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton('Меню')  # Название кнопки
        markup.add(item1)
        currency = ['USD', 'EUR', 'GBP', 'JPY', 'CNY','KZT','UAH','AED']
        markup.add(currency[0], currency[1])
        markup.add(currency[2], currency[3])
        markup.add(currency[4], currency[5])
        markup.add(currency[6], currency[7])
        self.bot.send_message(message.chat.id, 'Выберите валюту:', reply_markup=markup)

    def show_value_info(self, message, currency):
        self.selected_currency = currency
        self.bot.send_message(message.chat.id, f'Выбранная валюта: {currency}')

    def get_currency_info(self, message):
        driver = webdriver.Chrome()
        driver.get('https://cbr.ru/eng/currency_base/daily/')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('table', {'class': 'data'})
        rows = table.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            cols = [col.text.strip() for col in cols]
            if cols:
                    if cols[1] == self.selected_currency:
                        self.bot.send_message(message.chat.id, f'{cols[1]} = {cols[4]}, по отношению к рублю')
        driver.close()


    #БЛОК МЕТАЛЛОВ
    def show_metal_menu(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton('Меню')  # Название кнопки
        markup.add(item1)
        markup.add (self.metal[0], self.metal[1])
        markup.add(self.metal[2], self.metal[3])
        self.bot.send_message(message.chat.id, 'Выберите металл:', reply_markup=markup)

    def show_metal_info(self, message, metal):
        self.selected_metal = metal
        self.bot.send_message(message.chat.id, f'Информация о металле: {metal}')

    def get_metal_info(self, message):
        driver = webdriver.Chrome()
        driver.get('https://cbr.ru/eng/hd_base/metall/metall_base_new/#highlight=metals')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('table', {'class': 'data'})
        rows = table.find_all('tr')
        ic(rows)
        for row in rows:
            value = row.find_all('td')
            value = [val.text.strip() for val in value if val.text.strip()]
            if len(value) == 0:
                continue
            self.bot.send_message(message.chat.id, f'{self.selected_metal} = {value[self.metal.index(self.selected_metal) + 1]} Рублей за грамм')
            break
        driver.quit()

    #БЛОК АКЦИЙ
    def show_stock_menu(self, message):

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Меню')  # Название кнопки
        markup.add(item1)
        for metal in self.stocks:
            markup.add(types.KeyboardButton(metal))
        self.bot.send_message(message.chat.id, 'Выберите акцию:', reply_markup=markup)

    def show_stock_info(self, message, stock):
        self.selected_stock = stock
        self.bot.send_message(message.chat.id, f'Выбранная акция: {stock}')

    def get_stock_info(self, message):
        url = f'https://finnhub.io/api/v1/quote?symbol={self.selected_stock}&token={self.API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            self.bot.send_message(message.chat.id, f'Цена акции: {data["c"]}')
            return data['c']
        else:
            self.bot.send_message(message.chat.id, f'Ошибка: {response.status_code}')



    # БЛОК ИНФОРМАЦИИ
    def show_info(self, message):

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        items = [types.KeyboardButton('Меню'), types.KeyboardButton('Пункт 1'), types.KeyboardButton('Пункт 2'),
                 types.KeyboardButton('Пункт 3'), types.KeyboardButton('Пункт 4')]
        messages = ['Я расскажу вам о своем функционале', '1-е. Я могу показать актуальный курс валюты',
                    '2-е. Я могу показать актуальный курс металлов', '3-е. Я могу показать актуальную цену акций',
                    '4-е. Я могу показать дополнительную информацию']
        actions = ['typing', 'typing', 'typing', 'typing', 'typing']

        markup.row(items[0])
        markup.row(items[1], items[2])
        markup.row(items[3], items[4])

        for i in range(len(messages)):
            self.bot.send_message(message.chat.id, messages[i])
            self.bot.send_chat_action(message.chat.id, actions[i])

        self.bot.send_message(message.chat.id,
                              'Если вас заинтересовал какой-то пункт, напишите цифру в чат или выберите ее в меню',
                              reply_markup=markup)


    def run(self):

        self.bot.polling()


bot = Bot('6733330904:AAHCIv4ER8E769rU8VqKyi6qHACyFCHGmGM')
bot.run()

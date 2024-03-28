
import time
import telebot
from telebot import types, formatting
from tinkoff.invest import Client


TOKEN = ''
bot = telebot.TeleBot(TOKEN)
tokens = dict()
values = dict()


@bot.message_handler(commands=['start'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_1 = types.KeyboardButton('Мой readonly токен')
    item_2 = types.KeyboardButton('Инфа по тиньку')
    markup.add(item_1, item_2)
    
    bot.send_message(message.chat.id, 'Wellcum', reply_markup=markup)

 
@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == 'Мой readonly токен':
        if message.chat.id not in tokens:
            bot.send_message(message.chat.id, 'Дай токен')
        else:
            bot.send_message(message.chat.id, tokens[message.chat.id])
    elif len(message.text) > 25:
        tokens[message.chat.id] = message.text
    elif message.text == 'Инфа по тиньку':
        while True:
            with Client(tokens[message.chat.id]) as client:
                temp = 0
                accounts = client.users.get_accounts()
                out = 'Наименование | Стоимость за 1 ед. | % 12ч | Прибыль\n'
                for id in [acc.id for acc in accounts.accounts]:
                    pos = client.operations.get_portfolio(account_id=id)
                    positions = pos.positions
                    for p in positions:
                        r = client.instruments.find_instrument(query=p.figi)
                        price = p.current_price
                        win = p.expected_yield
                        for i in r.instruments:
                            if i.name not in values:
                                values[i.name] = price.units
                            else:
                                temp = round((values[i.name] - price.units)/values[i.name]*100, 5)
                                values[i.name] = price.units
                            out += '-------------------------------------------------\n'
                            out += f'{i.name:<15} | {price.units:<10.2f} | {temp:<8}% | {win.units}\n'
                bot.send_message(message.chat.id, formatting.hcode(out), parse_mode='HTML')
                time.sleep(43200)
            


bot.polling(none_stop=True, interval=0)

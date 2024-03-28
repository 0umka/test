import telebot
from tinkoff.invest import Client
from telebot import types

TOKEN = ''

bot = telebot.TeleBot(TOKEN)


tokens = dict()


@bot.message_handler(commands=['start'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_1 = types.KeyboardButton('Мой readonly токен')
    item_2 = types.KeyboardButton('Инфа по портфелям')
    item_3 = types.KeyboardButton('Позиции на счете')
    item_4 = types.KeyboardButton('Общая стоимость')
    item_5 = types.KeyboardButton('Стрим позиций портфеля')
    markup.add(item_1, item_2, item_3, item_4, item_5)
    
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
    elif message.text == 'Инфа по портфелям':
        with Client(tokens[message.chat.id]) as client:
            accounts = client.users.get_accounts()
            for id in [acc.id for acc in accounts.accounts]:
                bot.send_message(message.chat.id, f'Id портфеля: {id}')
                bot.send_message(message.chat.id, f'Общая стоимость акций в портфеле: {client.operations.get_portfolio(account_id=id).total_amount_shares.units}')
                bot.send_message(message.chat.id, f'Общая стоимость облигаций в портфеле: {client.operations.get_portfolio(account_id=id).total_amount_bonds.units}')
                bot.send_message(message.chat.id, f'Общая стоимость фондов в портфеле: {client.operations.get_portfolio(account_id=id).total_amount_etf.units}')
                bot.send_message(message.chat.id, f'Общая стоимость валют в портфеле: {client.operations.get_portfolio(account_id=id).total_amount_currencies.units}')
                bot.send_message(message.chat.id, f'Общая стоимость фяючерсов в портфеле: {client.operations.get_portfolio(account_id=id).total_amount_futures.units}')
                bot.send_message(message.chat.id, f'Текущая относительная доходность портфеля: {client.operations.get_portfolio(account_id=id).expected_yield.nano/1e+8} %')
    elif message.text == 'Общая стоимость':
        with Client(tokens[message.chat.id]) as client:
            accounts = client.users.get_accounts()
            for id in [acc.id for acc in accounts.accounts]:
                bot.send_message(message.chat.id, f'Общая стоимость портфеля {id}: {client.operations.get_portfolio(account_id=id).total_amount_portfolio.units}')
    elif message.text == 'Стрим позиций портфеля':
        with Client(tokens[message.chat.id]) as client:
            response = client.users.get_accounts()
            accounts = [acc.id for acc in response.accounts]
            for response in client.operations_stream.positions_stream(accounts=accounts):
                bot.send_message(message.chat.id, f'{id}: {response}')
                

bot.polling(none_stop=True, interval=0)

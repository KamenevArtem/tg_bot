import telebot
import os
import pathlib
from telebot import types
from dotenv import load_dotenv

load_dotenv()
access_token = os.environ['TG_API_KEY']
bot = telebot.TeleBot(access_token)


def send_image(bot, call, pic_number):
    script_path = pathlib.Path.cwd()
    file_path = script_path.joinpath(f'media/posy_{pic_number}.jpg')
    with open(file_path, 'rb') as posting_file:
        bot.send_photo(chat_id=call.message.chat.id, photo=posting_file)


@bot.message_handler(commands=['start'])
def start(message):
    message_to_customer = f'<b>{message.from_user.first_name}</b>, к какому событию готовитесь? Выберите один из вариантов, либо укажите свой'
    markup = types.InlineKeyboardMarkup()
    bday_button = types.InlineKeyboardButton('День рождения', callback_data= 'occ_birthday')
    wedding_button = types.InlineKeyboardButton('Свадьба', callback_data= 'occ_wedding')
    school_button = types.InlineKeyboardButton('Школа', callback_data= 'occ_school')
    other_occation_button = types.InlineKeyboardButton('Другой повод', callback_data= 'occ_other')
    markup.add(bday_button, wedding_button, school_button, other_occation_button)
    bot.send_message(message.chat.id, message_to_customer, 
                      parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('occ'))
def handle_occation(call):
    prices = [
        '~500', '~1000', '~2000', 'больше', 'не важно'
        ]
    if call.data == 'occ_birthday':
        markup = types.InlineKeyboardMarkup(row_width=3)
        for price in prices:
            markup.add(types.InlineKeyboardButton(f'{price}', callback_data=f'price {price}'))
        bot.send_message(call.message.chat.id, 'Вы готовитесь ко дню рождения, на какую сумму вы рассчитываете?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'occ_wedding':
        markup = types.InlineKeyboardMarkup(row_width=3)
        for price in prices:
            markup.add(types.InlineKeyboardButton(f'{price}', callback_data=f'price {price}'))
        bot.send_message(call.message.chat.id, 'Вы готовитесь к свадьбе, на какую сумму вы рассчитываете?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'occ_school':
        markup = types.InlineKeyboardMarkup(row_width=3)
        for price in prices:
            markup.add(types.InlineKeyboardButton(f'{price}', callback_data=f'price {price}'))
        bot.send_message(call.message.chat.id, 'Вы готовитесь к школе, на какую сумму вы рассчитываете?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'occ_other':
        markup = types.InlineKeyboardMarkup(row_width=3)
        for price in prices:
            markup.add(types.InlineKeyboardButton(f'{price}', callback_data=f'price {price}'))
        bot.send_message(call.message.chat.id, 'У вас другой повод, на какую сумму вы рассчитываете?',
                         parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('price'))
def handle_price(call):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    order = types.KeyboardButton(text='Заказать букет')
    other = types.KeyboardButton(text='Другое')
    markup.add(order, other)
    if call.data == 'price ~500':
        pic_number = '1'
        real_price = '485'
        send_image(bot, call, pic_number)
        bot.send_message(call.message.chat.id, f'Ваш букет, стоимостью {real_price}', parse_mode='html', reply_markup=markup)
    elif call.data == 'price ~1000':
        pic_number = '2'
        real_price = '867'
        send_image(bot, call, pic_number)
        bot.send_message(call.message.chat.id, f'Ваш букет, стоимостью {real_price}', parse_mode='html', reply_markup=markup)
    elif call.data == 'price ~2000':
        pic_number = '3'
        real_price = '1658'
        send_image(bot, call, pic_number)
        bot.send_message(call.message.chat.id, f'Ваш букет, стоимостью {real_price}', parse_mode='html', reply_markup=markup)
    elif call.data == 'price больше':
        pic_number = '4'
        real_price = '2100'
        send_image(bot, call, pic_number)
        bot.send_message(call.message.chat.id, f'Ваш букет, стоимостью {real_price}', parse_mode='html', reply_markup=markup)
    elif call.data == 'price не важно':
        pic_number = '5'
        real_price = '2341'
        send_image(bot, call, pic_number)
        bot.send_message(call.message.chat.id, f'Ваш букет, стоимостью {real_price}', parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_bouquet(message):
    if message.text == 'Заказать букет':
        bot.send_message(message.chat.id, f'Ваш заказ будет передан курьеру. Напишите ваши данные: имя, адрес, предпочтительное время доставки.')
    elif message.text == 'Другое':
        message_to_customer = 'Хотите что-то еще более уникальное? Подберите другой букет из нашей коллекции или закажите консультацию флориста.'
        markup = types.InlineKeyboardMarkup(row_width=1)
        consultation = types.InlineKeyboardButton(text='Консультация специалиста', callback_data='fin_consultation')
        collection = types.InlineKeyboardButton(text='Посмотреть коллекцию', callback_data='fin_collection')
        cancel = types.InlineKeyboardButton(text='Отменить', callback_data='fin_cancel')
        markup.add(consultation, collection, cancel)
        bot.send_message(message.chat.id, message_to_customer, parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('fin'))
def handle_price(call):
    if call.data == 'fin_consultation':
        bot.send_message(call.message.chat.id, 'Укажите номер телефона, и наш флорист перезвонит Вам в течение 20 минут.', parse_mode='html')
    elif call.data == 'fin_collection':
        pic_quantity = 5
        for pic_number in range(1, pic_quantity):
            send_image(bot, call, str(pic_number))
    elif call.data == 'fin_cancel':
        bot.send_message(call.message.chat.id, 'Если хотите выбрать другой букет, напишите сообщение "/start".')


if __name__ == "__main__":
    bot.polling(non_stop=True)

from ast import In
import asyncio
from cgitb import text
from email import message
from time import sleep
from weakref import WeakValueDictionary
from select import select
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bs4 import BeautifulSoup 
from bestchange_api import BestChange
from aiogram.types.input_file import InputFile
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from threading import Thread
import os
from time import sleep
from random import randint

def delete_cache():
    while True:
        sleep(7200)
        try:
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'info.zip')
            os.remove(path)
        except:
            pass

t = Thread(target=delete_cache)
t.start()

bot_name = "x-exchange.ru"
bot = Bot(token="5354793143:AAEp-cnM2LqihIYGcyCnvURqAW9nxvDYeeg")

dp = Dispatcher(bot, storage=MemoryStorage())

order = {
}
orders = []
reservs_dict = {}

class Form(StatesGroup):
    price_sum = State()

class PayData(StatesGroup):
    user_email = State()
    user_pay_method = State()


# Менять здесь!
#Наши кошельки крипты
btc_address = 'bc1q66s83w39y0tcflcr67e5jr0uxyc43txhzgaj8v'
eth_address = '0x608d21D2191838783F7bC509ee91DBC2e849504a'
ltc_address = 'ltc1qkrety9rzy0rwrwzmmd38k8ta6kq3eeeghpd7es'
bch_address = 'qz2vafqjzkxaysuzk80gyztxhlgqdxc00yjlu9dpxq'
etc_address = '0xbDaD1ab702b32F2177836Bd77850Df23fa5Ae166'
xrp_address = ''
xmr_address = '0xe935A6C549A777e9187814217d6880C4e14f58F9'
doge_address = 'DGFvkcSnyWbSqFVt8BtLv9LJbARVDg9e1W'
dash_address = 'Xv2wLr354ThrVDMXqgF7fB7YpNkEDAKnf8'
usdt_trc_address = 'THyQHhXvTCgbyB4NPzN8ZMP4fc9dYULF1M'
usdt_erc_address = '0x608d21D2191838783F7bC509ee91DBC2e849504a'
usdt_bep_address = '0xA26C27668cB69Ab70fB0Fe363E027027bF8A35D0'
trx_address = 'THyQHhXvTCgbyB4NPzN8ZMP4fc9dYULF1M'
bnb_address = '0xA26C27668cB69Ab70fB0Fe363E027027bF8A35D0'
sol_address = 'Bd4ZauE6MXctqjfQDuiTH8M2QRefHLLXhyayQHv1Jggu'
ton_address = '0xA26C27668cB69Ab70fB0Fe363E027027bF8A35D0'
#Наши банковские карты
sber_card = '2200730247698950'
tinkoff_card = '2200730247698950'
vtb_card = '2200730247698950'
alpha_card = '2200730247698950'
sbp_card = '+79220389654'
mir_card = '2200730247698950'
visamc_card = '2200730247698950'
#Наши кошельки
advcash_wallet = ''
payeer_wallet = ''
perfectm_wallet = ''
webm_wallet = ''
youm_wallet = ''
qiwi_wallet = '+79220389654'

# Резервы



# Нижние кнопки
extange = KeyboardButton("✅ Обменять")
help_ = KeyboardButton('❓Помощь')
contacts = KeyboardButton('📱 Контакты')
reservs = KeyboardButton('💵 Резервы')
user_main_id = KeyboardButton('👤 Личный кабинет') 
main_greed_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(extange, help_).row(contacts, reservs).row(user_main_id)

# оплачено

paid = InlineKeyboardButton("Оплачено", callback_data='paid')
paid_kb = InlineKeyboardMarkup(row_width=1).add(paid)

# назад

back = InlineKeyboardButton('Назад', callback_data='back')
back_kb = InlineKeyboardMarkup.add(back)

# Выбор способа
crypto_type = ['BTC', 'ETH', 'LTC', 'BCH', 'ETC', 'XRP', 'XMR', 'DOGE', 'DASH', 'USDT ERC20', 'USDT TRC20', 'USDT BEP20', 'TRX', 'BNB', 'SOL', 'TON']
bank_type = ['Промсвязьбанк',
'Почта Банк',
'Открытие',
'Совкомбанк',
'Росбанк',
'Газпромбанк','VISA/MC', "МИР", "Альфа Банк", "СБП", "ВТБ", "Тинькофф", "Сбербанк", 'Альфа Банк UAH', 'Райффайзен UAH', 'Укрсиббанк UAH', 'Приват24 UAH', 'Ощадбанк UAH', 'Jysan Bank KZT', 'Сбербанк KZT', 'Центр Кредит KZT', 'Альфа Банк KZT', 'HalykBank KZT', 'ForteBank KZT', 'Kaspi Bank KZT']
pay_sys_type = ["AdvCash", "Payeer", "PerfectMoney USD", "Webmoney", "ЮMoney", "QIWI"]

crypto = InlineKeyboardButton("Криптовалюта", callback_data='crypto')
bank = InlineKeyboardButton("Банки", callback_data='banks')
pay_sys = InlineKeyboardButton("Платежные Системы", callback_data='pay_sys')
pay_type = InlineKeyboardMarkup(row_width=1).add(crypto, bank, pay_sys, back)


# crypro
bitcoin = InlineKeyboardButton("BTC", callback_data='btc')
ethereum = InlineKeyboardButton("ETH", callback_data="eth")
litecoin = InlineKeyboardButton("LTC", callback_data='ltc')
bch = InlineKeyboardButton('BCH', callback_data='bch')
etc = InlineKeyboardButton('ETC', callback_data='etc')
xrp = InlineKeyboardButton('XRP', callback_data='xrp')
xmr = InlineKeyboardButton('XMR', callback_data='xmr')
doge = InlineKeyboardButton('DOGE', callback_data='doge')
dash = InlineKeyboardButton('DASH', callback_data='dash')
usdt_erc = InlineKeyboardButton('USDT ERC20', callback_data='usdt_erc') 
usdt_trc = InlineKeyboardButton('USDT TRC20', callback_data='usdt_trc') 
usdt_bep = InlineKeyboardButton('USDT BEP20', callback_data='usdt_bep') 
trx = InlineKeyboardButton('TRX', callback_data='trx')
bnb = InlineKeyboardButton('BNB', callback_data='bnb')
sol = InlineKeyboardButton('SOL', callback_data='sol')
ton = InlineKeyboardButton('TON', callback_data='ton')
crypto_pay = InlineKeyboardMarkup(row_width=2).add(bitcoin, ethereum, litecoin, bch, etc, xrp, xmr, doge, dash, usdt_trc, usdt_erc, usdt_bep, trx, bnb, sol, ton, back)

# bank
sber = InlineKeyboardButton("Сбербанк", callback_data='sber')
tinkoff = InlineKeyboardButton("Тинькофф", callback_data='tinkoff')
vtb = InlineKeyboardButton("ВТБ", callback_data='vtb')
sbp = InlineKeyboardButton("СБП", callback_data='sbp')
alpha = InlineKeyboardButton("Альфа Банк", callback_data='alpha')
promsv = InlineKeyboardButton('Промсвязьбанк', callback_data="promsv")
postbank = InlineKeyboardButton('Почта Банк', callback_data='postbank')
openbank = InlineKeyboardButton('Открытие', callback_data='openbank')
sovcombank = InlineKeyboardButton('Совкомбанк',callback_data='sovcombank')
rosbank = InlineKeyboardButton('Росбанк', callback_data='rosbank')
gazprom = InlineKeyboardButton('Газпромбанк', callback_data='gazprom')
mir = InlineKeyboardButton("МИР", callback_data="mir")
vm = InlineKeyboardButton('VISA/MC', callback_data="vm")
alpha_uah = InlineKeyboardButton('Альфа Банк UAH', callback_data='alpha_uah')
raif_uah = InlineKeyboardButton('Райффайзен UAH', callback_data='raif_uah')
ukrsib = InlineKeyboardButton('Укрсиббанк UAH', callback_data='ukrsib')
privat24 = InlineKeyboardButton('Приват24 UAH', callback_data='privat24')
oshad = InlineKeyboardButton('Ощадбанк UAH', callback_data='oshad')
jusan = InlineKeyboardButton('Jysan Bank KZT', callback_data='jusan')
sber_kzt = InlineKeyboardButton('Сбербанк KZT', callback_data='sber_kzt')
centr_kzt = InlineKeyboardButton('Центр Кредит KZT', callback_data='centr_kzt')
alpha_kzt = InlineKeyboardButton('Альфа Банк KZT', callback_data='alpha_kzt')
halk = InlineKeyboardButton('HalykBank KZT', callback_data='halk')
forte = InlineKeyboardButton('ForteBank KZT', callback_data='forte')
kaspi = InlineKeyboardButton('Kaspi Bank KZT', callback_data='kaspi')

bank_pay = InlineKeyboardMarkup(row_width=2).add(sber, tinkoff, vtb, sbp, alpha, promsv, postbank, openbank, sovcombank, rosbank, gazprom, mir, vm, alpha_uah, raif_uah, ukrsib, privat24, oshad, jusan, sber_kzt, centr_kzt, alpha_kzt, halk, forte, kaspi, back)

# pay_sys
qiwi = InlineKeyboardButton("QIWI", callback_data='qiwi')
youm = InlineKeyboardButton("ЮMoney", callback_data='youm')
webm = InlineKeyboardButton("Webmoney", callback_data='webm')
perfectm = InlineKeyboardButton("PerfectMoney USD", callback_data="perfectm")
payeer = InlineKeyboardButton("Payeer", callback_data="payeer")
advcash = InlineKeyboardButton("AdvCash", callback_data="advcash")

pay_sys_pay = InlineKeyboardMarkup(row_width=2).add(qiwi, youm, webm, perfectm, payeer, advcash, back)

def parser_reservs():
    req = requests.get('https://x-exchange.ru/reserve/')
    soup = BeautifulSoup(req.text, 'lxml')
    blocks = soup.find_all('div', {"class" : "one_reserv_block"})
    for i in blocks:
        reservs_dict[i.find('div', 'one_reserv_title').text] = i.find('div', 'one_reserv_sum').text


def converter(a, b):
    ids = {
    'BTC' : '93',
    'ETH' : '139',
    'USDT TRC20' : '10',
    'USDT ERC20' : '36',
    'USDT BEP20' : '208',
    'BNB' : '19',
    'BCH' : '172', 
    'ETC' : '160',
    'XRP' : '161',
    'XMR' : '149',
    'DOGE': '115',
    'DASH': '140',
    'TRX' : '185',
    'SOL' : '82',
    'TON' : '209',
    'LTC' : '99',
    'QIWI' : '63',
    'ЮMoney' : '6',
    'Сбербанк':'42',
    'Тинькофф':'105',
    'ВТБ':'51',
    'СБП' : '21', 
    'Альфа Банк' : '52',
    'МИР' : '17', 
    'VISA/MC' : '59',
    "Webmoney" : '1', 
    "PerfectMoney USD" : '40', 
    "Payeer" : '117',
    "AdvCash" : '121', 
    'Промсвязьбанк' : '53', 
    'Почта Банк' : '170',
    'Открытие' : '176',
    'Совкомбанк' : '34',
    'Росбанк' : '195',
    'Газпромбанк' : '95',
    'Альфа Банк UAH' : '37',
    'Райффайзен UAH' : '158',
    'Укрсиббанк UAH' : '22',
    "Приват24 UAH" : '56',
    "Ощадбанк UAH" : '68',
    'Jysan Bank KZT' : '207',
    'Сбербанк KZT' : '114',
    'Центр Кредит KZT' : '114',
    'Альфа Банк KZT' : '114', 
    'HalykBank KZT' : '90', 
    'ForteBank KZT' : '75', 
    'Kaspi Bank KZT' : '66'

}
    api = BestChange(load=True, cache=True, cache_seconds=10000, cache_path='./')
    exchangers = api.exchangers().get()

    dir_from = int(ids[a])
    dir_to = int(ids[b])
    rows = api.rates().filter(dir_from, dir_to)
    title = 'Exchange rates in the direction (https://www.bestchange.ru/index.php?from={}&to={}) {} : {}'
    print(title.format(dir_from, dir_to, api.currencies().get_by_id(dir_from), api.currencies().get_by_id(dir_to)))
    for val in rows[:1]:
        if ids[b] == '63' or ids[b] == '6' or ids[b] == '42' or ids[b] == '105' or ids[b] == '51' or ids[b] == '21' or ids[b] == '52' or ids[b] == '17' or ids[b] == '59' or ids[b] == '1'or ids[b] == '40' or ids[b] == '117' or ids[b] == '121'  or ids[b] == '66' or ids[b] == '75' or ids[b] == '90' or ids[b] == '114' or ids[b] == '207' or ids[b] == '68' or ids[b] == '56' or ids[b] == '22' or ids[b] == '158' or ids[b] == '37':
            return [val['give'], round(float(val['get']), 2)]
        elif ids[a] == '63' or ids[a] == '6' or ids[a] == '42' or ids[a] == '105' or ids[a] == '51' or ids[a] == '21' or ids[a] == '52' or ids[a] == '17' or ids[a] == '59' or ids[a] == '1'or ids[a] == '40' or ids[a] == '117' or ids[a] == '121' or ids[a] == '66' or ids[a] == '75' or ids[a] == '90' or ids[a] == '114' or ids[a] == '207' or ids[a] == '68' or ids[a] == '56' or ids[a] == '22' or ids[a] == '158' or ids[a] == '37':
            return [round(float(val['give']), 2), val['get']]
        else:
            return [val['give'], val['get']]


@dp.message_handler(commands=['start'])
async def echo_message(msg: types.Message):
    user_id = msg.from_user.id
    print(msg.chat.id)
    await bot.send_message(msg.from_user.id, f"🤖 Рады приветствовать вас в нашем боте!\n\n💰 Отличный курс\n🗂 Множество направлений\n💸 Быстрый вывод \n🎁 Акции каждую неделю\n💳 Большой выбор банков\n\n\n👨‍💻Ваш персональный id: {user_id}\n\n‼️Если бот не отвечает, введите команду /start для перезапуска", reply_markup=main_greed_kb)

    await bot.send_sticker(msg.from_user.id, 'CAACAgIAAxkBAAEFuF9jDmWewaeRGtGmrI8gO1n_-YmPyQACGAYAApb6EgUXxjuEbqBBESkE')
    order[user_id] = {
        'first_pos': 'BTC',
        'second_pos': 'Тинькофф', 
        'first_price' : 0,
        'second_price' : 0,
        'old_first_price' : 0,
        'old_second_price' : 0,
        'now' : 0,
        'user_email' : '',
        'user_pay_method' : '',
    }
    price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
    order[user_id]['first_price'] = price[0]
    order[user_id]['second_price'] = price[1]
    order[user_id]['old_first_price'] = price[0]
    order[user_id]['old_second_price'] = price[1]
    #await bot.delete_message(msg.from_user.id, msg.message_id)
    # Main menu
    first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
    replacement = InlineKeyboardButton("🔄", callback_data="replacement")
    second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
    first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
    d4c = InlineKeyboardButton("↔️", callback_data='d4c')
    second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
    pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
    start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
    order_kb = InlineKeyboardMarkup(row_width=3).add(
        first_pos, replacement, second_pos, first_price, d4c,  second_price)
    order_kb.row(pay_data)
    order_kb.row(start_order)
    await bot.send_message(msg.from_user.id, f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}\n\nPrice: {order[user_id]["first_price"]} {order[user_id]["first_pos"]} - {order[user_id]["second_price"]} {order[user_id]["second_pos"]}', reply_markup=order_kb)

@dp.message_handler(text = '❓Помощь')
async def comands_buttons(msg: types.Message):
    await bot.send_message(msg.from_user.id, '/start - начать работу\n/cancle - прервать ввод')
@dp.message_handler(text = '✅ Обменять')
async def comands_buttons(msg: types.Message):
    user_id = msg.from_user.id
    first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
    replacement = InlineKeyboardButton("🔄", callback_data="replacement")
    second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
    first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
    d4c = InlineKeyboardButton("↔️", callback_data='d4c')
    second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
    pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
    start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
    order_kb = InlineKeyboardMarkup(row_width=3).add(
        first_pos, replacement, second_pos, first_price, d4c,  second_price)
    order_kb.row(pay_data)
    order_kb.row(start_order)
    await bot.send_message(msg.from_user.id, f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}\n\nPrice: {order[user_id]["first_price"]} {order[user_id]["first_pos"]} - {order[user_id]["second_price"]} {order[user_id]["second_pos"]}', reply_markup=order_kb)
@dp.message_handler(text = '📱 Контакты')
async def comands_buttons(msg: types.Message):
    await bot.send_message(msg.from_user.id, '☎️Контакты\n\n✉️ Служба поддержки:\n@x_exchange_ru\nsupport@x-exchange.ru\n\n👉 Наш сайт: x-exchange.ru')
@dp.message_handler(text = '💵 Резервы')
async def comands_buttons(msg: types.Message):
    user_id = msg.from_user.id
    first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
    replacement = InlineKeyboardButton("🔄", callback_data="replacement")
    second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
    first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
    d4c = InlineKeyboardButton("↔️", callback_data='d4c')
    second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
    pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
    start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
    order_kb = InlineKeyboardMarkup(row_width=3).add(
        first_pos, replacement, second_pos, first_price, d4c,  second_price)
    order_kb.row(pay_data)
    order_kb.row(start_order)
    order_kb.row(back)
    data = "Резервы:"
    parser_reservs()
    for i in reservs_dict:
        data = data + f'\n{i.replace(" ", "").split()[0]} - {reservs_dict[i].replace(" ", "").split()[0]}'
    print(data)
    await bot.send_message(msg.from_user.id, data, reply_markup=order_kb)

@dp.message_handler(text = '👤 Личный кабинет')
async def comands_buttons(msg: types.Message):
    user_id = msg.from_user.id
    await bot.send_message(msg.from_user.id, f'Пользователь {user_id}\nСтатус: активен\nБан: нет')

@dp.callback_query_handler(text=['set_pay_data'])
async def pay_data_settings(call: types.CallbackQuery):
    user_id = call.from_user.id
    if call.data == 'set_pay_data':
        await call.message.answer("✉️Введите свой Телеграм\n (Например @x_exchange_ru)")
        await PayData.user_email.set()

@dp.message_handler(state=PayData.user_email)
async def process_email(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if '@' in message.text:
        async with state.proxy() as data:
            order[user_id]['user_email'] = data['user_email'] = message.text
            print(order[user_id]['user_email'])
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, "❗️Введенные данные указаны некоректно")
        await state.finish()
    global breaker
    if order[user_id]['second_pos'] in crypto_type:
        breaker = 1
        await message.reply("Добавьте адрес своего крипто кошелька\nНапример bc1qspnkzq73dy8jszm6gkjqn6v0stntzt0p28zng2")  
    if order[user_id]['second_pos'] in bank_type:
        breaker = 2
        await message.reply("Добавьте номер банковской карты для получения перевода")
    if order[user_id]['second_pos'] in pay_sys_type:
        breaker = 3
        await message.reply("Добавьте номер электронного кошелька")
    await PayData.user_pay_method.set()
    

@dp.message_handler(state=PayData.user_pay_method)
async def process_wallet(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if breaker == 1 and len(message.text) > 20:
        async with state.proxy() as data:
            order[user_id]['user_pay_method'] = data['user_pay_method'] = message.text
            print(order[user_id]['user_pay_method'])
        await state.finish()
    elif breaker == 2 and len(message.text.replace(' ', '')) == 16 and int(message.text.replace(' ', '')):
        async with state.proxy() as data:
            order[user_id]['user_pay_method'] = data['user_pay_method'] = message.text
            print(order[user_id]['user_pay_method'])
        await state.finish()
    elif breaker == 3:
        async with state.proxy() as data:
            order[user_id]['user_pay_method'] = data['user_pay_method'] = message.text
            print(order[user_id]['user_pay_method'])
        await state.finish()
    else:
        print(breaker)
        await bot.send_message(message.from_user.id, "❗️Введеные данные не верны")
        await state.finish()
    first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
    replacement = InlineKeyboardButton("🔄", callback_data="replacement")
    second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
    first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
    d4c = InlineKeyboardButton("↔️", callback_data='d4c')
    second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
    pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
    start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
    order_kb = InlineKeyboardMarkup(row_width=3).add(
        first_pos, replacement, second_pos, first_price, d4c,  second_price)
    order_kb.row(pay_data)
    order_kb.row(start_order)
    await message.reply(f"Отлично!\nПроверьте свои данные:\nTelegram: {order[user_id]['user_email']}\nСпособ оплаты:{order[user_id]['first_pos']} {order[user_id]['user_pay_method']}", reply_markup=order_kb)
    


@dp.callback_query_handler(text=['set_first_price', 'set_second_price'])
async def price_settigs(call: types.CallbackQuery):
    user_id = call.from_user.id
    if call.data == 'set_first_price':
        order[user_id]['now'] = 1  
        await call.message.answer("Введите сумму: \n/cancel")
        await Form.price_sum.set()
    if call.data == 'set_second_price':
        order[user_id]['now'] = 2
        await call.message.answer("Введите сумму: \n/cancel")
        await Form.price_sum.set()

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')
    first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
    replacement = InlineKeyboardButton("🔄", callback_data="replacement")
    second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
    first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
    d4c = InlineKeyboardButton("↔️", callback_data='d4c')
    second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
    pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
    start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
    order_kb = InlineKeyboardMarkup(row_width=3).add(
        first_pos, replacement, second_pos, first_price, d4c,  second_price)
    order_kb.row(pay_data)
    order_kb.row(start_order)
    await message.reply('OK', reply_markup=order_kb)

@dp.message_handler(state=Form.price_sum)
async def process_price(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    async with state.proxy() as data:
        data['price_sum'] = message.text
        ids = {
    'BTC' : '93',
    'ETH' : '139',
    'USDT TRC20' : '10',
    'USDT ERC20' : '36',
    'USDT BEP20' : '208',
    'BNB' : '19',
    'BCH' : '172', 
    'ETC' : '160',
    'XRP' : '161',
    'XMR' : '149',
    'DOGE': '115',
    'DASH': '140',
    'TRX' : '185',
    'SOL' : '82',
    'TON' : '209',
    'LTC' : '99',
    'QIWI' : '63',
    'ЮMoney' : '6',
    'Сбербанк':'42',
    'Тинькофф':'105',
    'ВТБ':'51',
    'СБП' : '21', 
    'Альфа Банк' : '52',
    'МИР' : '17', 
    'VISA/MC' : '59',
    "Webmoney" : '1', 
    "PerfectMoney USD" : '40', 
    "Payeer" : '117',
    "AdvCash" : '121', 
    'Промсвязьбанк' : '53', 
    'Почта Банк' : '170',
    'Открытие' : '176',
    'Совкомбанк' : '34',
    'Росбанк' : '195',
    'Газпромбанк' : '95',
    'Альфа Банк UAH' : '37',
    'Райффайзен UAH' : '158',
    'Укрсиббанк UAH' : '22',
    "Приват24 UAH" : '56',
    "Ощадбанк UAH" : '68',
    'Jysan Bank KZT' : '207',
    'Сбербанк KZT' : '114',
    'Центр Кредит KZT' : '114',
    'Альфа Банк KZT' : '114', 
    'HalykBank KZT' : '90', 
    'ForteBank KZT' : '75', 
    'Kaspi Bank KZT' : '66'

}
        if order[user_id]['now'] == 1:
            if ids[order[user_id]['first_pos']] == '63' or ids[order[user_id]['first_pos']] == '6' or ids[order[user_id]['first_pos']] == '42' or ids[order[user_id]['first_pos']] == '105' or ids[order[user_id]['first_pos']] == '51' or ids[order[user_id]['first_pos']] == '21' or ids[order[user_id]['first_pos']] == '52' or ids[order[user_id]['first_pos']] == '17' or ids[order[user_id]['first_pos']] == '59' or ids[order[user_id]['first_pos']] == '1' or ids[order[user_id]['first_pos']] == '40' or ids[order[user_id]['first_pos']] == '117' or ids[order[user_id]['first_pos']] == '121'  or ids[order[user_id]['first_pos']] == '37' or ids[order[user_id]['first_pos']] == '158' or ids[order[user_id]['first_pos']] == '22' or ids[order[user_id]['first_pos']] == '56' or ids[order[user_id]['first_pos']] == '68' or ids[order[user_id]['first_pos']] == '207' or ids[order[user_id]['first_pos']] == '114' or ids[order[user_id]['first_pos']] == '90' or ids[order[user_id]['first_pos']] == '75' or ids[order[user_id]['first_pos']] == '66'  or ids[order[user_id]['first_pos']] == '53' or ids[order[user_id]['first_pos']] == '170' or ids[order[user_id]['first_pos']] == '176' or ids[order[user_id]['first_pos']] == '34' or ids[order[user_id]['first_pos']] == '195' or ids[order[user_id]['first_pos']] == '95':
                if float(data['price_sum']) < 1000:
                    await state.finish()
                    first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
                    replacement = InlineKeyboardButton("🔄", callback_data="replacement")
                    second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
                    first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
                    d4c = InlineKeyboardButton("↔️", callback_data='d4c')
                    second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
                    pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
                    start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
                    order_kb = InlineKeyboardMarkup(row_width=3).add(
                        first_pos, replacement, second_pos, first_price, d4c,  second_price)
                    order_kb.row(pay_data)
                    order_kb.row(start_order) 
                    await bot.send_message(message.from_user.id, "❗️Минимальная сумма ввода денежных средств для банков и платежных систем от 1000 р", reply_markup=order_kb)
                else:
                    try:
                        
                        float(data['price_sum'])
                        old_price = order[user_id]['old_first_price']
                        order[user_id]['first_price'] = data['price_sum']
                        if float(old_price) < float(order[user_id]['second_price']):
                            if ids[order[user_id]['second_pos']] == '63' or ids[order[user_id]['second_pos']] == '6' or ids[order[user_id]['second_pos']] == '42' or ids[order[user_id]['second_pos']] == '105' or ids[order[user_id]['second_pos']] == '51' or ids[order[user_id]['second_pos']] == '21' or ids[order[user_id]['second_pos']] == '52' or ids[order[user_id]['second_pos']] == '17' or ids[order[user_id]['second_pos']] == '59' or ids[order[user_id]['second_pos']] == '1' or ids[order[user_id]['second_pos']] == '40' or ids[order[user_id]['second_pos']] == '117' or ids[order[user_id]['second_pos']] == '121' or ids[order[user_id]['second_pos']] == '53' or ids[order[user_id]['second_pos']] == '170' or ids[order[user_id]['second_pos']] == '176' or ids[order[user_id]['second_pos']] == '34' or ids[order[user_id]['second_pos']] == '195' or ids[order[user_id]['second_pos']] == '95':
                                order[user_id]['second_price'] = str(round(float(order[user_id]['first_price']) * float(order[user_id]['old_second_price']), 2))
                            else:
                                order[user_id]['second_price'] = str(round(float(order[user_id]['first_price']) * float(order[user_id]['old_second_price']), 8))
                        elif float(old_price) > float(order[user_id]['second_price']):
                            if ids[order[user_id]['second_pos']] == '63' or ids[order[user_id]['second_pos']] == '6' or ids[order[user_id]['second_pos']] == '42' or ids[order[user_id]['second_pos']] == '105' or ids[order[user_id]['second_pos']] == '51' or ids[order[user_id]['second_pos']] == '21' or ids[order[user_id]['second_pos']] == '52' or ids[order[user_id]['second_pos']] == '17' or ids[order[user_id]['second_pos']] == '59' or ids[order[user_id]['second_pos']] == '1' or ids[order[user_id]['second_pos']] == '40' or ids[order[user_id]['second_pos']] == '117' or ids[order[user_id]['second_pos']] == '121' or ids[order[user_id]['second_pos']] == '53' or ids[order[user_id]['second_pos']] == '170' or ids[order[user_id]['second_pos']] == '176' or ids[order[user_id]['second_pos']] == '34' or ids[order[user_id]['second_pos']] == '195' or ids[order[user_id]['second_pos']] == '95':
                                # !!!Остановился здесь!!!
                                order[user_id]['second_price'] = str(round(float(order[user_id]['first_price']) / float(order[user_id]['old_first_price']), 2))
                            else:
                                order[user_id]['second_price'] = str(round(float(order[user_id]['first_price']) / float(order[user_id]['old_first_price']), 8))
                        print(order[user_id]['first_price'])
                        await state.finish()
                        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
                        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
                        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
                        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
                        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
                        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
                        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
                        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
                        order_kb = InlineKeyboardMarkup(row_width=3).add(
                            first_pos, replacement, second_pos, first_price, d4c,  second_price)
                        order_kb.row(pay_data)
                        order_kb.row(start_order) 
                        await bot.send_message(message.from_user.id, f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}\n\nPrice: {order[user_id]["first_price"]} {order[user_id]["first_pos"]} - {order[user_id]["second_price"]} {order[user_id]["second_pos"]}', reply_markup=order_kb)
                    except:
                        await state.finish()
                        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
                        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
                        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
                        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
                        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
                        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
                        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
                        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
                        order_kb = InlineKeyboardMarkup(row_width=3).add(
                            first_pos, replacement, second_pos, first_price, d4c,  second_price)
                        order_kb.row(pay_data)
                        order_kb.row(start_order) 
                        await bot.send_message(message.from_user.id, f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}\n\nPrice: {order[user_id]["first_price"]} {order[user_id]["first_pos"]} - {order[user_id]["second_price"]} {order[user_id]["second_pos"]}', reply_markup=order_kb)
            else:
                try:
                        
                    float(data['price_sum'])
                    old_price = order[user_id]['old_first_price']
                    order[user_id]['first_price'] = data['price_sum']
                    if float(old_price) < float(order[user_id]['second_price']):
                        if ids[order[user_id]['second_pos']] == '63' or ids[order[user_id]['second_pos']] == '6' or ids[order[user_id]['second_pos']] == '42' or ids[order[user_id]['second_pos']] == '105' or ids[order[user_id]['second_pos']] == '51' or ids[order[user_id]['second_pos']] == '21' or ids[order[user_id]['second_pos']] == '52' or ids[order[user_id]['second_pos']] == '17' or ids[order[user_id]['second_pos']] == '59' or ids[order[user_id]['second_pos']] == '1' or ids[order[user_id]['second_pos']] == '40' or ids[order[user_id]['second_pos']] == '117' or ids[order[user_id]['second_pos']] == '121':
                            order[user_id]['second_price'] = str(round(float(order[user_id]['first_price']) * float(order[user_id]['old_second_price']), 2))
                        else:
                            order[user_id]['second_price'] = str(round(float(order[user_id]['first_price']) * float(order[user_id]['old_second_price']), 8))
                    elif float(old_price) > float(order[user_id]['second_price']):
                        if ids[order[user_id]['second_pos']] == '63' or ids[order[user_id]['second_pos']] == '6' or ids[order[user_id]['second_pos']] == '42' or ids[order[user_id]['second_pos']] == '105' or ids[order[user_id]['second_pos']] == '51' or ids[order[user_id]['second_pos']] == '21' or ids[order[user_id]['second_pos']] == '52' or ids[order[user_id]['second_pos']] == '17' or ids[order[user_id]['second_pos']] == '59' or ids[order[user_id]['second_pos']] == '1' or ids[order[user_id]['second_pos']] == '40' or ids[order[user_id]['second_pos']] == '117' or ids[order[user_id]['second_pos']] == '121':
                            order[user_id]['second_price'] = str(round(float(order[user_id]['first_price']) / float(order[user_id]['old_first_price']), 2))
                        else:
                            order[user_id]['second_price'] = str(round(float(order[user_id]['first_price']) / float(order[user_id]['old_first_price']), 8))
                    print(order[user_id]['first_price'])
                    await state.finish()
                    first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
                    replacement = InlineKeyboardButton("🔄", callback_data="replacement")
                    second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
                    first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
                    d4c = InlineKeyboardButton("↔️", callback_data='d4c')
                    second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
                    pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
                    start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
                    order_kb = InlineKeyboardMarkup(row_width=3).add(
                        first_pos, replacement, second_pos, first_price, d4c,  second_price)
                    order_kb.row(pay_data)
                    order_kb.row(start_order) 
                    await bot.send_message(message.from_user.id, f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}\n\nPrice: {order[user_id]["first_price"]} {order[user_id]["first_pos"]} - {order[user_id]["second_price"]} {order[user_id]["second_pos"]}', reply_markup=order_kb)
                except:
                    await state.finish()
                    first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
                    replacement = InlineKeyboardButton("🔄", callback_data="replacement")
                    second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
                    first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
                    d4c = InlineKeyboardButton("↔️", callback_data='d4c')
                    second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
                    pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
                    start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
                    order_kb = InlineKeyboardMarkup(row_width=3).add(
                        first_pos, replacement, second_pos, first_price, d4c,  second_price)
                    order_kb.row(pay_data)
                    order_kb.row(start_order) 
                    await bot.send_message(message.from_user.id, f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}\n\nPrice: {order[user_id]["first_price"]} {order[user_id]["first_pos"]} - {order[user_id]["second_price"]} {order[user_id]["second_pos"]}', reply_markup=order_kb)
        elif order[user_id]['now'] == 2:
            if ids[order[user_id]['first_pos']] == '63' or ids[order[user_id]['first_pos']] == '6' or ids[order[user_id]['first_pos']] == '42' or ids[order[user_id]['first_pos']] == '105' or ids[order[user_id]['first_pos']] == '51' or ids[order[user_id]['first_pos']] == '21' or ids[order[user_id]['first_pos']] == '52' or ids[order[user_id]['first_pos']] == '17' or ids[order[user_id]['first_pos']] == '59' or ids[order[user_id]['first_pos']] == '1' or ids[order[user_id]['first_pos']] == '40' or ids[order[user_id]['first_pos']] == '117' or ids[order[user_id]['first_pos']] == '121'  or ids[order[user_id]['first_pos']] == '37' or ids[order[user_id]['first_pos']] == '158' or ids[order[user_id]['first_pos']] == '22' or ids[order[user_id]['first_pos']] == '56' or ids[order[user_id]['first_pos']] == '68' or ids[order[user_id]['first_pos']] == '207' or ids[order[user_id]['first_pos']] == '114' or ids[order[user_id]['first_pos']] == '90' or ids[order[user_id]['first_pos']] == '75' or ids[order[user_id]['first_pos']] == '66':
                if float(data['price_sum']) < 100:
                    await state.finish()
                    first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
                    replacement = InlineKeyboardButton("🔄", callback_data="replacement")
                    second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
                    first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
                    d4c = InlineKeyboardButton("↔️", callback_data='d4c')
                    second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
                    pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
                    start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
                    order_kb = InlineKeyboardMarkup(row_width=3).add(
                        first_pos, replacement, second_pos, first_price, d4c,  second_price)
                    order_kb.row(pay_data)
                    order_kb.row(start_order) 
                    await bot.send_message(message.from_user.id, "На банковские картах и платежных системы нельзя указывать количество меньше 1000", reply_markup=order_kb)
                else:
                    try:
                        float(data['price_sum'])
                        old_price = order[user_id]['old_second_price']
                        order[user_id]['second_price'] = data['price_sum']
                        if float(old_price) > float(order[user_id]['first_price']):
                            if ids[order[user_id]['first_pos']] == '63' or ids[order[user_id]['first_pos']] == '6' or ids[order[user_id]['first_pos']] == '42' or ids[order[user_id]['first_pos']] == '105' or ids[order[user_id]['first_pos']] == '51' or ids[order[user_id]['first_pos']] == '21' or ids[order[user_id]['first_pos']] == '52' or ids[order[user_id]['first_pos']] == '17' or ids[order[user_id]['first_pos']] == '59' or ids[order[user_id]['first_pos']] == '1' or ids[order[user_id]['first_pos']] == '40' or ids[order[user_id]['first_pos']] == '117' or ids[order[user_id]['first_pos']] == '121':
                                order[user_id]['first_price'] = str(round(float(order[user_id]['second_price']) / float(order[user_id]['old_second_price']), 2))
                            else:
                                order[user_id]['first_price'] = str(round(float(order[user_id]['second_price']) / float(order[user_id]['old_second_price']), 8))
                            print()
                        if float(old_price) < float(order[user_id]['first_price']):
                            if ids[order[user_id]['first_pos']] == '63' or ids[order[user_id]['first_pos']] == '6' or ids[order[user_id]['first_pos']] == '42' or ids[order[user_id]['first_pos']] == '105' or ids[order[user_id]['first_pos']] == '51' or ids[order[user_id]['first_pos']] == '21' or ids[order[user_id]['first_pos']] == '52' or ids[order[user_id]['first_pos']] == '17' or ids[order[user_id]['first_pos']] == '59' or ids[order[user_id]['first_pos']] == '1' or ids[order[user_id]['first_pos']] == '40' or ids[order[user_id]['first_pos']] == '117' or ids[order[user_id]['first_pos']] == '121':
                                order[user_id]['first_price'] = str(round(float(order[user_id]['second_price']) * float(order[user_id]['old_first_price']), 2))
                            else:
                                order[user_id]['first_price'] = str(round(float(order[user_id]['second_price']) * float(order[user_id]['old_first_price']), 8))
                        print(order[user_id]['second_price'])
                        await state.finish()
                        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
                        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
                        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
                        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
                        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
                        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
                        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
                        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
                        order_kb = InlineKeyboardMarkup(row_width=3).add(
                            first_pos, replacement, second_pos, first_price, d4c,  second_price)
                        order_kb.row(pay_data)
                        order_kb.row(start_order) 
                        await bot.send_message(message.from_user.id, f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}\n\nPrice: {order[user_id]["first_price"]} {order[user_id]["first_pos"]} - {order[user_id]["second_price"]} {order[user_id]["second_pos"]}', reply_markup=order_kb)
                    except:
                        await state.finish()
                        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
                        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
                        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
                        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
                        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
                        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
                        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
                        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
                        order_kb = InlineKeyboardMarkup(row_width=3).add(
                            first_pos, replacement, second_pos, first_price, d4c,  second_price)
                        order_kb.row(pay_data)
                        order_kb.row(start_order) 
                        await bot.send_message(message.from_user.id, f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}\n\nPrice: {order[user_id]["first_price"]} {order[user_id]["first_pos"]} - {order[user_id]["second_price"]} {order[user_id]["second_pos"]}', reply_markup=order_kb)
            else:
                try:
                    float(data['price_sum'])
                    old_price = order[user_id]['old_second_price']
                    order[user_id]['second_price'] = data['price_sum']
                    if float(old_price) > float(order[user_id]['first_price']):
                        if ids[order[user_id]['first_pos']] == '63' or ids[order[user_id]['first_pos']] == '6' or ids[order[user_id]['first_pos']] == '42' or ids[order[user_id]['first_pos']] == '105' or ids[order[user_id]['first_pos']] == '51' or ids[order[user_id]['first_pos']] == '21' or ids[order[user_id]['first_pos']] == '52' or ids[order[user_id]['first_pos']] == '17' or ids[order[user_id]['first_pos']] == '59' or ids[order[user_id]['first_pos']] == '1' or ids[order[user_id]['first_pos']] == '40' or ids[order[user_id]['first_pos']] == '117' or ids[order[user_id]['first_pos']] == '121':
                            order[user_id]['first_price'] = str(round(float(order[user_id]['second_price']) / float(order[user_id]['old_second_price']), 2))
                        else:
                            order[user_id]['first_price'] = str(round(float(order[user_id]['second_price']) / float(order[user_id]['old_second_price']), 8))
                        print()
                    if float(old_price) < float(order[user_id]['first_price']):
                        if ids[order[user_id]['first_pos']] == '63' or ids[order[user_id]['first_pos']] == '6' or ids[order[user_id]['first_pos']] == '42' or ids[order[user_id]['first_pos']] == '105' or ids[order[user_id]['first_pos']] == '51' or ids[order[user_id]['first_pos']] == '21' or ids[order[user_id]['first_pos']] == '52' or ids[order[user_id]['first_pos']] == '17' or ids[order[user_id]['first_pos']] == '59' or ids[order[user_id]['first_pos']] == '1' or ids[order[user_id]['first_pos']] == '40' or ids[order[user_id]['first_pos']] == '117' or ids[order[user_id]['first_pos']] == '121':
                            order[user_id]['first_price'] = str(round(float(order[user_id]['second_price']) * float(order[user_id]['old_first_price']), 2))
                        else:
                            order[user_id]['first_price'] = str(round(float(order[user_id]['second_price']) * float(order[user_id]['old_first_price']), 8))
                    print(order[user_id]['second_price'])
                    await state.finish()
                    first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
                    replacement = InlineKeyboardButton("🔄", callback_data="replacement")
                    second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
                    first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
                    d4c = InlineKeyboardButton("↔️", callback_data='d4c')
                    second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
                    pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
                    start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
                    order_kb = InlineKeyboardMarkup(row_width=3).add(
                        first_pos, replacement, second_pos, first_price, d4c,  second_price)
                    order_kb.row(pay_data)
                    order_kb.row(start_order) 
                    await bot.send_message(message.from_user.id, f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}\n\nPrice: {order[user_id]["first_price"]} {order[user_id]["first_pos"]} - {order[user_id]["second_price"]} {order[user_id]["second_pos"]}', reply_markup=order_kb)
                except:
                    await state.finish()
                    first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
                    replacement = InlineKeyboardButton("🔄", callback_data="replacement")
                    second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
                    first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
                    d4c = InlineKeyboardButton("↔️", callback_data='d4c')
                    second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
                    pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
                    start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
                    order_kb = InlineKeyboardMarkup(row_width=3).add(
                        first_pos, replacement, second_pos, first_price, d4c,  second_price)
                    order_kb.row(pay_data)
                    order_kb.row(start_order) 
                    await bot.send_message(message.from_user.id, f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}\n\nPrice: {order[user_id]["first_price"]} {order[user_id]["first_pos"]} - {order[user_id]["second_price"]} {order[user_id]["second_pos"]}', reply_markup=order_kb)

@dp.callback_query_handler(text=["start_order"])
async def start_order(message: types.message):
    user_id = message.from_user.id
    if order[user_id]['user_email'] == '' or order[user_id]['user_pay_method'] == '':
        await bot.send_message(message.from_user.id, "Заполните реквизиты!")
    else:
        data = f"От бота {bot_name} Заказ от {user_id}:\nПервая позиция: {order[user_id]['first_pos']}\nВторая позиция: {order[user_id]['second_pos']}\nКол-во первой позиции: {order[user_id]['first_price']}\nКол-во второй позиции: <code>{order[user_id]['second_price']}</code>\nEmail: {order[user_id]['user_email']}\nОтправка на {order[user_id]['second_pos']} <code>{order[user_id]['user_pay_method']}</code>"
        await bot.send_message(-630370144, data, parse_mode=types.ParseMode.HTML)
        if order[user_id]['first_pos'] in crypto_type:
            if order[user_id]['first_pos'] == 'BTC':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{btc_address}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == 'ETH':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{eth_address}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == 'LTC':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{ltc_address}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == 'BCH':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{bch_address}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == 'ETC':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{etc_address}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == 'USDT TRC20':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{usdt_trc_address}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == 'USDT ERC20':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{usdt_erc_address}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == 'USDT BEP20':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{usdt_bep_address}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == 'BNB':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{bnb_address}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == 'DOGE':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{doge_address}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == 'SOL':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{sol_address}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == 'TRX':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{trx_address}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == 'XRP':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{xrp_address}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == 'XMR':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{xmr_address}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == 'DASH':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{dash_address}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == 'TON':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{ton_address}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
        if order[user_id]['first_pos'] in bank_type:
            if order[user_id]['first_pos'] == "Сбербанк":
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{sber_card}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == "Тинькофф":
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{tinkoff_card}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == "ВТБ":
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{vtb_card}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == "Альфа Банк":
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{alpha_card}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == "СБП":
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{sbp_card}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == "МИР":
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{mir_card}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == "VISA/MC":
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{visamc_card}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
        if order[user_id]['first_pos'] in pay_sys_type:
            if order[user_id]['first_pos'] == 'QIWI':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{qiwi_wallet}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == 'ЮMoney':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{youm_wallet}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == 'Webmoney':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{webm_wallet}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == 'PerfectMoney USD':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{perfectm_wallet}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == 'Payeer':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{payeer_wallet}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
            if order[user_id]['first_pos'] == 'AdvCash':
                await bot.send_message(message.from_user.id, f"📋  Заявка №{randint(1000000, 1200000)}\n\n📌{order[user_id]['first_pos']} 🔄 {order[user_id]['second_pos']}\n\n⏱️  Завершите обмен в течении 30 минут\n\n➡️  Осуществите перевод на реквизиты ({order[user_id]['first_pos']})\n<code>{advcash_wallet}</code>\n\n➡️  На сумму:\n<code>{order[user_id]['first_price']}</code>\n\n➡️  Кошелек, куда Вы получаете:\n{order[user_id]['user_pay_method']}\n\n➡️  Сумма зачисления:\n{order[user_id]['second_price']}\n\n⬇️  После оплаты нажмите кнопку 'Оплачено'", reply_markup=paid_kb, parse_mode=types.ParseMode.HTML)
@dp.callback_query_handler(text=['paid'])    
async def paid_succes(msg: types.Message):
    user_id = msg.from_user.id
    await bot.send_message(-630370144, f"Заказ от {user_id} отмечен как оплаченый")
    await bot.send_message(msg.from_user.id, "⏳Заявка принята в обработку\n\nПожалуйста, ожидайте поступления\nСпасибо, что выбрали именно нас!")

@dp.callback_query_handler(text=['first_pos', 'replacement', 'second_pos'])
async def order_settings(call: types.CallbackQuery):
    user_id = call.from_user.id
    if call.data == 'replacement':
        order[user_id]['first_pos'], order[user_id]['second_pos'] = order[user_id]['second_pos'], order[user_id]['first_pos']
        order[user_id]['first_price'], order[user_id]['second_price'] = order[user_id]['second_price'], order[user_id]['first_price']
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"] }\n\nPrice: {order[user_id]["first_price"]} {order[user_id]["first_pos"]} - {order[user_id]["second_price"]} {order[user_id]["second_pos"]}', reply_markup=order_kb)
    elif call.data == 'first_pos':
        order[user_id]['now'] = 1
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"] }\n\nPrice: {order[user_id]["first_price"]} {order[user_id]["first_pos"]} - {order[user_id]["second_price"]} {order[user_id]["second_pos"]}', reply_markup=pay_type)
    elif call.data == 'second_pos':
        order[user_id]['now'] = 2
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"] }\n\nPrice: {order[user_id]["first_price"]} {order[user_id]["first_pos"]} - {order[user_id]["second_price"]} {order[user_id]["second_pos"]}', reply_markup=pay_type)

@dp.callback_query_handler(text=["crypto", "banks", "pay_sys", 'back'])
async def pay_type_settings(call: types.CallbackQuery):
    user_id = call.from_user.id
    if call.data == "crypto":
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=crypto_pay)
    if call.data == "banks":
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=bank_pay)
    if call.data == "pay_sys":
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=pay_sys_pay)
    if call.data == 'back':
        await call.message.delete()
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"] }\n\nPrice: {order[user_id]["first_price"]} {order[user_id]["first_pos"]} - {order[user_id]["second_price"]} {order[user_id]["second_pos"]}', reply_markup=order_kb)

@dp.callback_query_handler(text = ['btc', "eth", 'ltc',  'bch', 'etc', 'xrp', 'xmr', 'doge', 'dash', 'usdt_trc', 'usdt_erc', 'usdt_bep', 'trx', 'bnb', 'sol', 'ton'])
async def crypto_settings(call: types.CallbackQuery):
    global second_pos
    global first_pos
    user_id = call.from_user.id
    print(order[user_id]['now'])
    if call.data == 'back':
        await call.message.delete()
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"] }\n\nPrice: {order[user_id]["first_price"]} {order[user_id]["first_pos"]} - {order[user_id]["second_price"]} {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'btc':
        order[user_id]['first_pos'] = "BTC"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'eth':
        order[user_id]['first_pos'] = "ETH"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'ltc':
        order[user_id]['first_pos'] = "LTC"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'bch':
        order[user_id]['first_pos'] = "BCH"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'etc':
        order[user_id]['first_pos'] = "ETC"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'xrp':
        order[user_id]['first_pos'] = "XRP"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'xmr':
        order[user_id]['first_pos'] = "XMR"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'doge':
        order[user_id]['first_pos'] = "DOGE"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'dash':
        order[user_id]['first_pos'] = "DASH"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'usdt_trc':
        order[user_id]['first_pos'] = "USDT TRC20"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'usdt_erc':
        order[user_id]['first_pos'] = "USDT ERC20"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'usdt_bep':
        order[user_id]['first_pos'] = "USDT BEP20"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'trx':
        order[user_id]['first_pos'] = "TRX"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'bnb':
        order[user_id]['first_pos'] = "BNB"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'sol':
        order[user_id]['first_pos'] = "SOL"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'ton':
        order[user_id]['first_pos'] = "TON"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'btc':
        order[user_id]['second_pos'] = "BTC"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price') 
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")        
        order_kb = InlineKeyboardMarkup(row_width=3).add(
        first_pos, replacement, second_pos, first_price, second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'eth':
        order[user_id]['second_pos'] = "ETH"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'ltc':
        order[user_id]['second_pos'] = "LTC"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'bch':
        order[user_id]['second_pos'] = "BCH"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'etc':
        order[user_id]['second_pos'] = "ETC"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'xrp':
        order[user_id]['second_pos'] = "XRP"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'xmr':
        order[user_id]['second_pos'] = "XMR"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'doge':
        order[user_id]['second_pos'] = "DOGE"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'dash':
        order[user_id]['second_pos'] = "DASH"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'usdt_trc':
        order[user_id]['second_pos'] = "USDT TRC20"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'usdt_erc':
        order[user_id]['second_pos'] = "USDT ERC20"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'usdt_bep':
        order[user_id]['second_pos'] = "USDT BEP20"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'trx':
        order[user_id]['second_pos'] = "TRX"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'bnb':
        order[user_id]['second_pos'] = "BNB"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'sol':
        order[user_id]['second_pos'] = "SOL"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'ton':
        order[user_id]['second_pos'] = "TON"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    print(order[user_id]['second_pos'])

@dp.callback_query_handler(text = ['sber', "tinkoff", 'vtb', 'sbp', 'alpha', 'mir', 'vm', 'alpha_uah', 'raif_uah', 'ukrsib', 'privat24', 'oshad', 'jusan', 'sber_kzt', 'centr_kzt', 'alpha_kzt', 'halk', 'forte','kaspi'])
async def bank_settings(call: types.CallbackQuery):
    global second_pos
    global first_pos
    user_id = call.from_user.id
    if call.data == 'back':
        await call.message.delete()
        first_pos = InlineKeyboardButton(
            order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton(
            order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price') 
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")       
        order_kb = InlineKeyboardMarkup(row_width=3).add(
        first_pos, replacement, second_pos, first_price, second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"] }\n\nPrice: {order[user_id]["first_price"]} {order[user_id]["first_pos"]} - {order[user_id]["second_price"]} {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'sber':
        order[user_id]['first_pos'] = "Сбербанк"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'tinkoff':
        order[user_id]['first_pos'] = "Тинькофф"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'vtb':
        order[user_id]['first_pos'] = "ВТБ"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'sbp':
        order[user_id]['first_pos'] = "СБП"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'alpha':
        order[user_id]['first_pos'] = "Альфа Банк"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'mir':
        order[user_id]['first_pos'] = "МИР"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'vm':
        order[user_id]['first_pos'] = "VISA/MC"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'sber':
        order[user_id]['second_pos'] = "Сбербанк"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'tinkoff':
        order[user_id]['second_pos'] = "Тинькофф"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'vtb':
        order[user_id]['second_pos'] = "ВТБ"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'sbp':
        order[user_id]['second_pos'] = "СБП"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'alpha':
        order[user_id]['second_pos'] = "Альфа Банк"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'mir':
        order[user_id]['second_pos'] = "МИР"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'vm':
        order[user_id]['second_pos'] = "VISA/MC"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'alpha_uah':
        order[user_id]['second_pos'] = 'Альфа Банк UAH'
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'raif_uah':
        order[user_id]['second_pos'] = "Райффайзен UAH"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'ukrsib':
        order[user_id]['second_pos'] = "Укрсиббанк UAH"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'privat24':
        order[user_id]['second_pos'] = "Приват24 UAH"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'oshad':
        order[user_id]['second_pos'] = "Ощадбанк UAH"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'jusan':
        order[user_id]['second_pos'] = "Jysan Bank KZT"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'sber_kzt':
        order[user_id]['second_pos'] = "Сбербанк KZT"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'centr_kzt':
        order[user_id]['second_pos'] = "Центр Кредит KZT"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'alpha_kzt':
        order[user_id]['second_pos'] = "Альфа Банк KZT"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'halk':
        order[user_id]['second_pos'] = "HalykBank KZT"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'forte':
        order[user_id]['second_pos'] = "ForteBank KZT"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'kaspi':
        order[user_id]['second_pos'] = "Kaspi Bank KZT"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    

@dp.callback_query_handler(text = ['qiwi', 'youm', "advcash", "payeer", "perfectm", "'webm'"])
async def pay_sys_settings(call: types.CallbackQuery):
    global second_pos
    global first_pos
    user_id = call.from_user.id
    if call.data == 'back':
        await call.message.delete()
        first_pos = InlineKeyboardButton(
            order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton(
            order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price') 
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")       
        order_kb = InlineKeyboardMarkup(row_width=3).add(
        first_pos, replacement, second_pos, first_price, second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"] }\n\nPrice: {order[user_id]["first_price"]} {order[user_id]["first_pos"]} - {order[user_id]["second_price"]} {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'qiwi':
        order[user_id]['first_pos'] = "QIWI"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == 'youm':
        order[user_id]['first_pos'] = "ЮMoney"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == "advcash":
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'😢 К сожалению этот способ пока не доступен 😢\n\nПожалуйста, выберете другое направление\n\n🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == "payeer":
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'😢 К сожалению этот способ пока не доступен 😢\n\nПожалуйста, выберете другое направление\n\n🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == "perfectm":
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'😢 К сожалению этот способ пока не доступен 😢\n\nПожалуйста, выберете другое направление\n\n🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 1 and call.data == "webm":
        order[user_id]['first_pos'] = "Webmoney"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'qiwi':
        order[user_id]['second_pos'] = "QIWI"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == 'youm':
        order[user_id]['second_pos'] = "ЮMoney"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == "advcash":
        order[user_id]['second_pos'] = "AdvCash"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == "payeer":
        order[user_id]['second_pos'] = "Payeer"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == "perfectm":
        order[user_id]['second_pos'] = "PerfectMoney USD"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    if order[user_id]['now'] == 2 and call.data == "webm":
        order[user_id]['second_pos'] = "Webmoney"
        price = converter(order[user_id]['first_pos'], order[user_id]['second_pos'])
        order[user_id]['first_price'] = price[0]
        order[user_id]['second_price'] = price[1]
        order[user_id]['old_first_price'] = price[0]
        order[user_id]['old_second_price'] = price[1]
        first_pos = InlineKeyboardButton(order[user_id]['first_pos'], callback_data='first_pos')
        replacement = InlineKeyboardButton("🔄", callback_data="replacement")
        second_pos = InlineKeyboardButton( order[user_id]['second_pos'], callback_data='second_pos')
        first_price = InlineKeyboardButton(order[user_id]['first_price'], callback_data='set_first_price')
        d4c = InlineKeyboardButton("↔️", callback_data='d4c')
        second_price = InlineKeyboardButton(order[user_id]['second_price'], callback_data='set_second_price')  
        pay_data = InlineKeyboardButton("Добавить реквизиты", callback_data='set_pay_data')
        start_order = InlineKeyboardButton("Начать обмен", callback_data="start_order")      
        order_kb = InlineKeyboardMarkup(row_width=3).add(
            first_pos, replacement, second_pos, first_price, d4c,  second_price)
        order_kb.row(pay_data)
        order_kb.row(start_order) 
        await call.message.delete()
        await call.message.answer(f'🤖  Калькулятор\n\n📌 {order[user_id]["first_pos"]}   🔄    {order[user_id]["second_pos"]}', reply_markup=order_kb)
    

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)

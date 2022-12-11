import telebot
import requests
import bs4
import lxml
#bot.infinity_polling()
#bot.polling(none_stop = True)

bot = telebot.TeleBot("TOKEN", parse_mode=None)

# BTC
def get_BTC():
    link = 'https://coinmarketcap.com/currencies/bitcoin/'
    responce = requests.get(link).text
    soup = bs4.BeautifulSoup(responce, 'lxml')
    block = soup.find('div',"priceValue")
    status_data_block = block.find('span').text
    return status_data_block

# ETH
def get_ETH():
    link = 'https://coinmarketcap.com/currencies/ethereum/'
    responce = requests.get(link).text
    soup = bs4.BeautifulSoup(responce, 'lxml')
    block = soup.find('div',"priceValue")
    status_data_block = block.find('span').text
    return status_data_block

# USDT
def get_USDT():
    link = 'https://coinmarketcap.com/currencies/tether/'
    responce = requests.get(link).text
    soup = bs4.BeautifulSoup(responce, 'lxml')
    block = soup.find('div',"priceValue")
    status_data_block = block.find('span').text
    return status_data_block

# BNB
def get_BNB():
    link = 'https://coinmarketcap.com/currencies/bnb/'
    responce = requests.get(link).text
    soup = bs4.BeautifulSoup(responce, 'lxml')
    block = soup.find('div',"priceValue")
    status_data_block = block.find('span').text
    return status_data_block

# BUSD
def get_BUSD():
    link = 'https://coinmarketcap.com/currencies/binance-usd/'
    responce = requests.get(link).text
    soup = bs4.BeautifulSoup(responce, 'lxml')
    block = soup.find('div',"priceValue")
    status_data_block = block.find('span').text
    return status_data_block

# DOGE
def get_DOGE():
    link = 'https://coinmarketcap.com/currencies/dogecoin/'
    responce = requests.get(link).text
    soup = bs4.BeautifulSoup(responce, 'lxml')
    block = soup.find('div',"priceValue")
    status_data_block = block.find('span').text
    return status_data_block

# ADA
def get_ADA():
    link = 'https://coinmarketcap.com/currencies/cardano/'
    responce = requests.get(link).text
    soup = bs4.BeautifulSoup(responce, 'lxml')
    block = soup.find('div',"priceValue")
    status_data_block = block.find('span').text
    return status_data_block

# TRX 
def get_TRX():
    link = 'https://coinmarketcap.com/currencies/tron/'
    responce = requests.get(link).text
    soup = bs4.BeautifulSoup(responce, 'lxml')
    block = soup.find('div',"priceValue")
    status_data_block = block.find('span').text
    return status_data_block

# MATIC
def get_MATIC():
    link = 'https://coinmarketcap.com/currencies/polygon/'
    responce = requests.get(link).text
    soup = bs4.BeautifulSoup(responce, 'lxml')
    block = soup.find('div',"priceValue")
    status_data_block = block.find('span').text
    return status_data_block

# SOL
def get_SOL():
    link = 'https://coinmarketcap.com/currencies/solana/'
    responce = requests.get(link).text
    soup = bs4.BeautifulSoup(responce, 'lxml')
    block = soup.find('div',"priceValue")
    status_data_block = block.find('span').text
    return status_data_block


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard= True)
    item_BTC = telebot.types.KeyboardButton("BTC")
    item_ETH = telebot.types.KeyboardButton("ETH")
    item_USDT = telebot.types.KeyboardButton("USDT")
    item_BNB = telebot.types.KeyboardButton("BNB")
    item_BUSD = telebot.types.KeyboardButton("BUSD")
    item_DOGE = telebot.types.KeyboardButton("DOGE")
    item_ADA = telebot.types.KeyboardButton("ADA")
    item_TRX = telebot.types.KeyboardButton("TRX")
    item_MATIC = telebot.types.KeyboardButton("MATIC")
    item_SOL = telebot.types.KeyboardButton("SOL")
    
    markup.add(item_BTC, item_ETH, item_USDT, item_BNB, item_BUSD, item_DOGE, item_ADA, item_TRX, item_MATIC, item_SOL)

    bot.send_message(message.chat.id, "Hello, {0.first_name}, which cryptocurrency are you interested in?".format(message.from_user), reply_markup = markup)


@bot.message_handler(content_types=["text"])
def bot_message(message):
    if message.chat.type == "private":
        if message.text == "BTC":
            price_BTC = get_BTC()
            bot.send_message(message.chat.id, f"Price of BTC is {price_BTC}")

        elif message.text == "ETH":
            print_ETH = get_ETH()
            bot.send_message(message.chat.id, f"Price of ETH is {print_ETH}")

        elif message.text == "USDT":
            price_USDT = get_USDT()
            bot.send_message(message.chat.id, f"Price of USDT is {price_USDT}")

        elif message.text == "BNB":
            price_BNB = get_BNB()
            bot.send_message(message.chat.id, f"Price of BNB is {price_BNB}")

        elif message.text == "BUSD":
            price_BUSD = get_BUSD()
            bot.send_message(message.chat.id, f"Price of BUSD is {price_BUSD}")

        elif message.text == "DOGE":
            price_DOGE = get_DOGE()
            bot.send_message(message.chat.id, f"Price of DOGE is {price_DOGE}")

        elif message.text == "ADA":
            price_ADA = get_ADA()
            bot.send_message(message.chat.id, f"Price of ADA is {price_ADA}")

        elif message.text == "TRX":
            price_TRX = get_TRX()
            bot.send_message(message.chat.id, f"Price of TRX is {price_TRX}")
        
        elif message.text == "MATIC":
            price_MATIC = get_MATIC()
            bot.send_message(message.chat.id, f"Price of MATIC is {price_MATIC}")

        elif message.text == "SOL":
            price_SOL = get_SOL()
            bot.send_message(message.chat.id, f"Price of SOL is {price_SOL}")



#@bot.message_handler(commands=['help'])
#def send_welcome(message):
#    bot.reply_to(message, " All commands: \n start\n help\n BTC\n ETH\n USDT\n BNB\n BUSD\n DOGE\n ADA\n MATIC\n TRX\n SOL")    
#
#
#@bot.message_handler(func=lambda m: True)
#def echo_all(message):
#    bot.reply_to(message, message.text)
#


bot.infinity_polling()
bot.polling(none_stop = True)

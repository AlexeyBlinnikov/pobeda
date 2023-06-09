from dataclasses import replace
from xmlrpc.client import boolean
import requests
import json
import random
from bs4 import BeautifulSoup as BS
from pobeda import pobeda_gopro, pobeda_mac, pobeda_electro, pobeda_tent
import openai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentTypes
import aioschedule
import asyncio
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

TOKEN = "5134051967:AAEf72wUXntvg8ECcV-sarKJd3RtQWw-YIw"
# TOKEN = "5524654123:AAHfHmtyG1-s1G0JtZFbQX7FInrgh9fo50g"
openai.api_key = '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'
gopro_correct = []
mac_correct = []
electro_correct = []
tent_correct = []
passed_words = []
with open('word.txt', 'r') as r:
    text = r.read()
words = text.split("\n")



def price(x, x1, y, y1):
    url = "https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/check-price"
    headers = {
        "Accept-Language": "ru",
        "Authorization": "Bearer y0_AgAAAABpl9RLAAc6MQAAAADfnGEFEUkk2qFTSvmUUEKHr8LUx6_bXYY"
    }
    body = {
        "requirements": {
            "taxi_class": "express"},
        "route_points": [
            {"coordinates": [x, x1]}, #home 49.184220, 55.804538
            {"coordinates": [y, y1]} #korston 49.149962, 55.793728

      ],
        "skip_door_to_door": True
    }

    response = requests.post(url, data = json.dumps(body), headers=headers)
    # data = response.json()
    data = json.loads(response.content)
    # # price = data["result"]["price"]
    return float(data["price"])
    # print(x)

    
def english_words():
    word_today = random.sample(words, 5)
    return word_today
    


def bot():

    bot = Bot(token = TOKEN)
    dp = Dispatcher(bot)

    kb = ReplyKeyboardMarkup(resize_keyboard = True)
    kb0 = KeyboardButton('ЧатБот от OpenAI')
    kb.add(kb0)

    markup_in = InlineKeyboardMarkup(row_width = 1)
    kb_in = InlineKeyboardButton(text = 'Не беспокоить 2 часа', callback_data = 'two')
    kb_in2 = InlineKeyboardButton(text = 'Не беспокоить 12 часов', callback_data = 'twelve')
    markup_in.row(kb_in, kb_in2)

    hours = [1]


    @dp.message_handler(commands ='start')
    async def start(message: types.Message):
        await message.answer('Привет, бот запущен', reply_markup = kb)

    # Кулбэки
    @dp.callback_query_handler(Text(startswith='two'))
    async def call(callback: types.CallbackQuery):
        hours.insert(0, 2)
        await callback.answer('Уведомления отключены на 2 часа', show_alert= True)
    @dp.callback_query_handler(Text(startswith='twelve'))
    async def call(callback: types.CallbackQuery):
        hours.insert(0, 12)
        await callback.answer('Уведомления отключены на 12 часов', show_alert= True)

    @dp.callback_query_handler(lambda x: x.data and x.data.startswith('r '))
    async def kb_delete(call:types.CallbackQuery):
        try:
            w = call.data.replace('r ', '')
            words.remove(w)
            passed_words.remove(w)
            # await db_at_moment.del_sql(call.data.replace('del ', ''))
            await call.answer(text = f'Поздравляем, вы выучили слово {w}.', show_alert= True)
        except:
            await call.answer(text = f'Вы уже прошли данное слово - {w}.')

    @dp.callback_query_handler(lambda x: x.data and x.data.startswith('not_r '))
    async def kb_delete(call:types.CallbackQuery):
        try:
            ww = call.data.replace('not_r ', '')
            passed_words.remove(ww)
            await call.answer('Неправильно! Продолжайте обучение.')#, show_alert= True)
        except:
            await call.answer(text = f'Вы уже прошли данное слово - {ww}.')

    #Встроенные кнопки клавиатуры
    # @dp.message_handler(Text(equals = "Дом"))
    # async def sib(message: types.Message):
    # # if message.text == 'Ножи':
    #     await bot.send_message(message.from_user.id, f"Цена: {int(price(49.184220, 55.804538, 49.149962, 55.793728))}")
    # @dp.message_handler(lambda message: 'Центр' in message.text)
    # async def centr(message: types.Message):
    #     await bot.send_message(message.from_user.id, f"Цена: {int(price(49.127219, 55.777859, 49.184220, 55.804538))}")
    # @dp.message_handler(lambda message: 'Квартал' in message.text)
    # async def kvartal(message: types.Message):
    #     await bot.send_message(message.from_user.id, f"Цена: {int(price(49.107492, 55.819975, 49.184220, 55.804538))}")
    # @dp.message_handler(lambda message: 'Проспект' in message.text)
    # async def prospect(message: types.Message):
    #     await bot.send_message(message.from_user.id, f"Цена: {int(price(49.200809, 55.753747, 49.184220, 55.804538))}")

    @dp.message_handler(Text(equals = "ЧатБот от OpenAI"))
    async def start(message: types.Message):
        await bot.send_message(message.from_user.id, "Для общения с ChatGpt - начинай диалог с 'Gpt' и бот ответит на любые твои вопросы")

    #отправляем смс при высокой цене
    # async def home():
    #     if price(49.184220, 55.804538, 49.149962, 55.793728) > 300:
    #             await bot.send_message(377590850, f"Братишка, + {int(price(49.184220, 55.804538, 49.149962, 55.793728)-90)} руб к заказу, если тебе нечего делать, иди поработай.", reply_markup = markup_in)
    #информация о наличии объявлений по go pro с сайта победы
    # async def go_pro():
    #     if pobeda_gopro() != inname[-1]:
    #         inname.append(pobeda_gopro())
    #         await bot.send_message(377590850, f"Победа: {pobeda_gopro()}")

    async def go_pro():
        try:
            if pobeda_gopro() not in gopro_correct:
                gopro_correct.append(pobeda_gopro())
                await bot.send_message(377590850, f"Победа: {pobeda_gopro()}")
        except Exception as ex:
            await bot.send_message(377590850, f"Ошибка (победа Go pro): {ex}")
    async def mac():
        try:
            if pobeda_mac() not in mac_correct:
                mac_correct.append(pobeda_mac())
                await bot.send_message(377590850, f"Победа: {pobeda_mac()}")
        except Exception as ex:
            await bot.send_message(377590850, f"Ошибка (Мак): {ex}")
    async def electro():
        try:
            if pobeda_electro() not in electro_correct:
                electro_correct.append(pobeda_electro())
                await bot.send_message(377590850, f"Победа: {pobeda_electro()}")
        except Exception as ex:
            await bot.send_message(377590850, f"Ошибка (победа самокат): {ex}")
    async def tent():
        try:
            if pobeda_tent() not in tent_correct:
                tent_correct.append(pobeda_tent())
                await bot.send_message(377590850, f"Победа: {pobeda_tent()}")
        except Exception as ex:
            await bot.send_message(377590850, f"Ошибка (победа палатки): {ex}")



    #5 английских слов
    async def english():
        await bot.send_message(377590850, "Слова для изучения:")
        for i in english_words():
            await bot.send_message(377590850, f"{i.title()}")
            await asyncio.sleep(1)
            # words.remove(i)
            passed_words.append(i)

    async def test_passed_words():
        try:
        # await bot.send_message(377590850, f"Тест пройденных слов  {len(passed_words)}")
            for i in passed_words:
                lo = 0
                # print(i)
                x = i.split("—")
                y = random.choice(words).split("—")
                z = random.choice(words).split("—")
                t = random.choice(words).split("—")

                kb_word1 = InlineKeyboardButton(f"{x[-1]}", callback_data = f"r {i}")
                kb_word2 = InlineKeyboardButton(f"{y[-1]}", callback_data = f'not_r {i}')
                kb_word3 = InlineKeyboardButton(f"{z[-1]}", callback_data = f'not_r {i}')
                kb_word4 = InlineKeyboardButton(f"{t[-1]}", callback_data = f'not_r {i}')

                rand_answer = [kb_word1, kb_word2, kb_word3, kb_word4]
                random.shuffle(rand_answer)
                x_final = x[0].split(' ')
                await bot.send_message(377590850, f"    {x_final[0].title()}", reply_markup =InlineKeyboardMarkup().add(rand_answer[0]).insert(rand_answer[1]).add(rand_answer[2]).insert(rand_answer[3]))

        except:
            words.remove(i)
            passed_words.remove(i)
            await bot.send_message(377590850, f"Из-за ошибки удалил данное слово, просто запомни его: {i}")

    @dp.message_handler(Text(contains = 'gpt', ignore_case = True))
    async def start(message: types.Message):
        try:
            arg = message.text
            for i in arg.split(' '):
                if i.lower() == 'gpt' or i.lower() == 'gpt,':
                    arg = arg.replace(i, '')

    # model_engine = "text-davinci-003"
            completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", 
                    messages=[{
                            "role": "user", 
                            "content": f"{arg}"}])

            response = completion.choices[0].message.content
            await bot.send_message(message.from_user.id, f'{response}')
            # await message.reply(arg)
        except Exception as ex:
            await bot.send_message(message.from_user.id, f'Вероятно, кончился бесплатный лимит: {ex}')



    async def scheduler():
        aioschedule.every(10).minutes.do(go_pro)
        aioschedule.every().day.at("08:30").do(english)
        aioschedule.every(40).minutes.do(mac)
        aioschedule.every(20).minutes.do(tent)
        aioschedule.every(22).minutes.do(electro)
        aioschedule.every().day.at("18:30").do(test_passed_words)
        while True:
            await aioschedule.run_pending()
            if hours[0] == 2:
                await asyncio.sleep(7200)
                hours.insert(0, 1)
            if hours[0] == 12:
                await asyncio.sleep(40000)
                hours.insert(0, 1)
            await asyncio.sleep(1)

    async def on_startup(_):
        asyncio.create_task(scheduler())

    executor.start_polling(dp, skip_updates = True, on_startup = on_startup)

if __name__ == "__main__":
    bot()
# price(49.184220, 55.804538, 49.149962, 55.793728)


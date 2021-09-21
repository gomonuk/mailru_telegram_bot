import os
import subprocess

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils import executor
from dotenv import load_dotenv

import reverse_polish_notation as rpn

load_dotenv()

TOKEN = os.environ.get("TG_BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

CACHE = {}


async def cache_set(user_id, value, answer):
    if not user_id:
        return
    cached_value = CACHE.get(user_id) or []
    if len(cached_value) == 5:
        cached_value.pop(0)

    cached_value.append({"value": value, "answer": answer})
    CACHE[user_id] = cached_value


@dp.message_handler(commands=["start", "help"])
async def welcome_handler(msg: types.Message):
    await msg.reply(
        f"Привет, {msg.from_user.first_name}! \n"
        f"Бот обрабатывает только положительные числа от 0 до 9, "
        f"и операторы {' '.join(i for i in rpn.PRIORITY_MAP.keys())}"
        f"Команда /history показывает пять последних операций"
    )


@dp.callback_query_handler(filters.Text(startswith="num_"))
async def history_callback(call: types.CallbackQuery):
    value = call.data.split("_")[1]
    user_id = call.from_user.values.get("id")
    history = CACHE.get(user_id, [])
    answer = [i["answer"] for i in history if i["value"] == value][0]
    await call.message.answer(answer)
    await call.answer()


@dp.message_handler(commands=["history", "h"])
async def history_handler(msg: types.Message):
    user_id = msg.from_user.values.get("id")
    buttons = [
        types.InlineKeyboardButton(text=i["value"], callback_data=f"num_{i['value']}")
        for i in reversed(CACHE.get(user_id, []))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await msg.answer("history", reply_markup=keyboard)


@dp.message_handler(content_types=["text"])
async def calc_handler(msg: types.Message):
    answer = "Что-то пошло не так"
    user_id = msg.from_user.values.get("id")
    value = msg.text.lower()

    if value:
        list_of_items, error = rpn.string_normalization(value)
        if error:
            await msg.answer(error)
            return

        rpn_list = rpn.create_rpn(list_of_items)
        if 3 > len(rpn_list):  # Минимум должно быть два операнда и один оператор
            await msg.answer("Ошибка парсинга выражения, может быть вы ввели ерунду?")
            return

        answer = rpn.exec_rpn(rpn_list)
        await cache_set(user_id, value, answer)

    await msg.answer(answer)


if __name__ == "__main__":
    subprocess.Popen(["python", "server.py"])
    executor.start_polling(dp)

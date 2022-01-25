import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.sql.expression import text
from config import TOKEN
from request_db import DBComands
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import markups
from myexeptions import NulValue
class DataInput(StatesGroup):
    read = State()

bot =  Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
date_base = DBComands()

@dp.message_handler(commands=["start"])
async def register_user(message: types.Message):
    chat_id = message.from_user.id
    refereal = message.get_args()
    if refereal == '':
        refereal = None
    else:
        refereal = int(refereal)
    user_name = message.from_user.first_name
    full_name = message.from_user.full_name
    date_base.add_new_user(chat_id, user_name, full_name, refereal)
    await bot.send_message(message.from_user.id, text = markups.btn_main_menu.text , reply_markup=markups.main_menu)

#@dp.message_handler(commands=["add_money"])
async def get_free_money(message: types.Message):
    if date_base.time_update(message.from_user.id)[1]:
        date_base.update_balance_user(message.from_user.id, 100)
        await bot.send_message(message.from_user.id, text = f"полученно 100  {date_base.view_balance_user(message.from_user.id)}")

    else:
        await bot.send_message(message.from_user.id, text = f"Следующее получение через 10 секунд - прошло: {date_base.time_update(message.from_user.id)[0]}")


#@dp.message_handler(commands=["get_money"])
async def get_job_money(message: types.Message):
    bot_username = (await bot.me).username
    bot_link = f"https://t.me/{bot_username}?start={message.from_user.id}"
    text1 = f"""
Ваша реферальная ссылка: {bot_link}
$ Баланс {date_base.view_balance_user(message.from_user.id)}
Всего приглашено: {date_base.count_referal_user(message.from_user.id)}.
"""

    await bot.send_message(message.from_user.id, text = text1, reply_markup=markups.get_money_menu)

@dp.message_handler(state=DataInput.read)
async def cash(message: types.Message, state: FSMContext):
     try:
        sum_set = int(message.text)
        a = date_base.set_moey_user(message.from_user.id, sum_set)
        await message.answer(f"{a}")
     except ValueError:

         await message.answer(f"вы ничего не ввели")
         await state.finish()
        
     
     await state.finish()


@dp.message_handler()
async def command_start(message: types.Message):

    if  message.text == "Получить $":
        #await bot.send_message(message.from_user.id, message.text, reply_markup=markups.main_menu)
        await get_free_money(message)
    elif message.text == "Главное меню":
        await bot.send_message(message.from_user.id, message.text, reply_markup=markups.main_menu)
    elif message.text == "Отмена":
        await bot.send_message(message.from_user.id, message.text, reply_markup=markups.get_money_menu)

    elif message.text == "Вывод $":
        text_view = """
        введите сумму которую вы хотите вывести
        """
        await bot.send_message(message.from_user.id, text=text_view, reply_markup=markups.returt_main_menu)
        
        await DataInput.read.set()
    elif message.text == "Заработать $":
        await get_job_money(message)
        #await bot.send_message(message.from_user.id, text = text2, reply_markup=markups.get_money_menu)
           
    elif message.text == "Конкурс":
        await bot.send_message(message.from_user.id, message.text, reply_markup=markups.main_menu)

    else:
        await bot.send_message(message.from_user.id, text="Нет такой коанды нажмите введите /start", reply_markup=markups.main_menu)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
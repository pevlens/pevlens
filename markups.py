from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


btn_compitition = KeyboardButton("Конкурс")
btn_receive_money = KeyboardButton("Получить $")
btn_get_money = KeyboardButton("Заработать $")
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_compitition, btn_get_money,btn_receive_money)



btn_withdrawal_money = KeyboardButton("Вывод $")
btn_main_menu = KeyboardButton("Главное меню")
get_money_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_withdrawal_money, btn_main_menu)


btn_cancel = KeyboardButton("Отмена")
returt_main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_cancel)

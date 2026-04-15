import logging
import asyncio
import os
import pyautogui
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from wakeonlan import send_magic_packet

# --- КОНФИГУРАЦИЯ ---
API_TOKEN = '8708390823:AAGy5_6J-vtlYbEX14QsaLGy3FdmQ29L-m8'
ADMIN_ID = 1970457251  # Твой ID
# В Python для WoL лучше использовать двоеточия в MAC-адресе
TARGET_MAC = 'D4:3D:7E:E1:07:86'  
PC_PASSWORD = "1979" # Твой пароль

logging.basicConfig(level=logging.INFO)

# Исправлено под новую версию aiogram 3.7+
bot = Bot(
    token=API_TOKEN, 
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()

# --- КЛАВИАТУРА ---
def get_main_kb():
    buttons = [
        # Исправлено: было callback_input, должно быть callback_data
        [InlineKeyboardButton(text="🚀 Включить ПК (WoL)", callback_data="pc_on")],
        [InlineKeyboardButton(text="🔑 Ввести пароль", callback_data="pc_pass")],
        [InlineKeyboardButton(text="🛑 Выключить ПК", callback_data="pc_off")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# --- ОБРАБОТЧИКИ ---

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("<b>⛔ Доступ запрещен.</b>")
    
    await message.answer(
        f"<b>👋 Привет, Хозяин!</b>\n\n"
        f"Компьютер ожидает команд. Выбери действие ниже: 👇",
        reply_markup=get_main_kb()
    )

@dp.callback_query(F.data == "pc_on")
async def wake_pc(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    
    # Отправляем магический пакет
    send_magic_packet(TARGET_MAC)
    
    await callback.answer("Сигнал Wake-on-LAN отправлен! ⚡", show_alert=True)
    await callback.message.edit_text(
        "<b>🚀 Команда отправлена!</b>\nЖду, пока ПК загрузится до экрана блокировки...",
        reply_markup=get_main_kb()
    )

@dp.callback_query(F.data == "pc_pass")
async def enter_password(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    
    await callback.answer("Ввожу пароль... ⏳")
    
    # Эмуляция ввода: кликаем Enter, чтобы убрать заставку, ждем и вводим
    pyautogui.press('enter')
    await asyncio.sleep(1.5) 
    pyautogui.write(PC_PASSWORD, interval=0.1)
    pyautogui.press('enter')
    
    await callback.message.answer("<b>🔑 Попытка входа выполнена!</b>\nЕсли пароль верный, рабочий стол открыт.")

@dp.callback_query(F.data == "pc_off")
async def shutdown_pc(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    
    await callback.answer("Выключаю... 😴")
    await callback.message.edit_text("<b>🛑 Компьютер завершает работу.</b>")
    
    # Выключение через 5 секунд
    os.system("shutdown /s /t 5")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот остановлен!")
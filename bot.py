import logging
import asyncio
import os
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from wakeonlan import send_magic_packet

# ================= НАСТРОЙКИ =================
TOKEN = '8708390823:AAGy5_6J-vtlYbEX14QsaLGy3FdmQ29L-m8'
ADMIN_ID = 1970457251
TARGET_MAC = 'D4-3D-7E-E1-07-86'
# =============================================

logging.basicConfig(level=logging.INFO)

# Инициализация бота с поддержкой HTML
bot = Bot(
    token=TOKEN, 
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()

# Кнопки управления
def get_main_kb():
    buttons = [
        [InlineKeyboardButton(text="🚀 ВКЛЮЧИТЬ (WoL)", callback_data="pc_on")],
        [InlineKeyboardButton(text="🛑 ВЫКЛЮЧИТЬ (Force)", callback_data="pc_off")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Команда /start
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return # Игнорируем чужих
    
    await message.answer(
        "<b>🖥 Панель управления ПК</b>\n\n"
        "Выбери действие ниже: 👇",
        reply_markup=get_main_kb()
    )

# Обработка нажатия "Включить"
@dp.callback_query(F.data == "pc_on")
async def wake_pc(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    
    send_magic_packet(TARGET_MAC)
    await callback.answer("Сигнал отправлен! ⚡")
    await callback.message.answer("<b>✅ Magic Packet отправлен на MAC-адрес.</b>")

# Обработка нажатия "Выключить"
@dp.callback_query(F.data == "pc_off")
async def shutdown_pc(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    
    await callback.answer("Выключаю... 😴")
    await callback.message.answer("<b>🔴 ПК выключается прямо сейчас!</b>")
    
    # Прямая команда Windows для мгновенного выключения без вопросов
    if sys.platform == "win32":
        os.system(r"C:\Windows\System32\shutdown.exe /s /f /t 0")
    else:
        # Для Linux/Hosting серверов (если запустишь там, попробует выключить сервер)
        os.system("shutdown -h now")

async def main():
    # Удаляем вебхуки и запускаем опрос сервера
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот выключен")
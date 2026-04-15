import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from wakeonlan import send_magic_packet

# --- КОНФИГУРАЦИЯ ---
TOKEN = '8708390823:AAGy5_6J-vtlYbEX14QsaLGy3FdmQ29L-m8'
ADMIN_ID = 1970457251
TARGET_MAC = 'D4:3D:7E:E1:07:86'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Кнопки
def main_kb():
    buttons = [
        [InlineKeyboardButton(text="🚀 ВКЛЮЧИТЬ", callback_data="pc_on")],
        [InlineKeyboardButton(text="🛑 ВЫКЛЮЧИТЬ", callback_data="pc_off")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(Command("start"))
async def start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("<b>🖥 Управление питанием ПК:</b>", reply_markup=main_kb())

@dp.callback_query(F.data == "pc_on")
async def on(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    send_magic_packet(TARGET_MAC)
    await callback.answer("Сигнал WoL отправлен! ⚡")
    await callback.message.answer("<b>✅ Команда на включение отправлена!</b>")

@dp.callback_query(F.data == "pc_off")
async def off(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    await callback.answer("Выключаю... 😴")
    await callback.message.answer("<b>🔴 Компьютер выключается (через 5 сек).</b>")
    # Обычное системное выключение Windows
    os.system("shutdown /s /t 5")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# --- መረጃዎችን እዚህ ይተኩ ---
TOKEN = "8380663114:AAFff3_NSD7PMhHghRAbNI11KsgqFDL8EXY"
ADMIN_ID = 8412701064  # ያንተን የቴሌግራም ID ቁጥር እዚህ አስገባ
# ----------------------------

dp = Dispatcher()

class ArizStates(StatesGroup):
    language = State()
    company_name = State()
    receipt_photo = State()

texts = {
    'አማርኛ': {
        'welcome': "እንኳን ወደ አሪዝ መተግበሪያ አሪዞ ቴክ (ሸቃይ) የክፍያ ማዘመኛ ሲስተም በደህና መጡ።\n\nእባክዎን አሪዝ መተግበሪያ ላይ የተመዘገቡበትን የድርጅት ስምዎን ያስገቡ፡",
        'get_photo': "እባክዎ ክፍያ ያስገቡበትን ደረሰኝ የፎቶ ምስል ይላኩ!",
        'thanks': "እናመስግናለን! ወርሃዊ የአሪዝ ቴክ (ሸቃይ) መተግበሪያ ሲስተምዎ በጥቂት ደቂቃ ውስጥ ክፍት ይሆናል እናመስግናለን! \n\nሀሳብ አስተያየት ካለዎት @ArizMediaProduction ላይ ይፃፉልን።"
    },
    'English': {
        'welcome': "Welcome to Ariz App (ArizTech) Payment Update System.\n\nPlease enter your Company Name registered on Ariz App:",
        'get_photo': "Please send a photo of your payment receipt!",
        'thanks': "Thank you! Your ArizTech system will be activated within a few minutes. \n\nFor feedback, contact @ArizMediaProduction"
    }
}

@dp.message(CommandStart())
async def command_start_handler(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="አማርኛ"), KeyboardButton(text="English")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("ቋንቋ ይምረጡ / Choose Language:", reply_markup=kb)
    await state.set_state(ArizStates.language)

@dp.message(ArizStates.language)
async def process_language(message: types.Message, state: FSMContext):
    if message.text not in ["አማርኛ", "English"]:
        await message.answer("እባክዎ ከታች ካሉት ይምረጡ / Please choose from below")
        return
    
    await state.update_data(lang=message.text)
    await message.answer(texts[message.text]['welcome'], reply_markup=ReplyKeyboardRemove())
    await state.set_state(ArizStates.company_name)

@dp.message(ArizStates.company_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(c_name=message.text)
    data = await state.get_data()
    await message.answer(texts[data['lang']]['get_photo'])
    await state.set_state(ArizStates.receipt_photo)

@dp.message(ArizStates.receipt_photo, F.photo)
async def process_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    # ለአንተ መረጃውን መላክ
    await message.bot.send_message(
        ADMIN_ID, 
        f"🔔 አዲስ ክፍያ ተልኳል!\n🏢 ድርጅት: {data['c_name']}\n👤 ተጠቃሚ: @{message.from_user.username or 'No Username'}"
    )
    await message.bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    
    await message.answer(texts[data['lang']]['thanks'])
    await state.clear()

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())  


    # ከላይ ካሉት import መስመሮች ጋር ይህንን ይጨምሩ
from aiogram.client.session.aiohttp import AiohttpSession

# ... ሌሎች ኮዶች እንዳሉ ሆነው ...

async def main():
    # ለነፃው PythonAnywhere አካውንት የሚያስፈልግ Proxy
    session = AiohttpSession(proxy="http://proxy.server:3128")
    
    # ቦቱን በProxy አማካኝነት ማስነሳት
    bot = Bot(token=TOKEN, session=session)
    await dp.start_polling(bot)
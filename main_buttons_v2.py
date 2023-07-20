import os

import logging
import asyncio

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command, CommandObject, Text
from aiogram.types import Message
from dotenv import load_dotenv
from aiogram import html
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from settings import config

logger = logging.getLogger(__name__)
# Bot token can be obtained via https://t.me/BotFahter

load_dotenv()

# Dispatcher is a root router
dp = Dispatcher()

# All handlers should be attached to the Router (or Dispatcher)
router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="З пюрешкою"),
            types.KeyboardButton(text="З окрошкою"),
            types.KeyboardButton(text="З борщем"),

        ],
        [
            types.KeyboardButton(text="Без пюрешки"),
            types.KeyboardButton(text="Без окрошки"),
            types.KeyboardButton(text="Без борщу"),
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=False,
        one_time_keyboard=True,
        input_field_placeholder="Виберіть спосіб подачі",
    )
    await message.answer("Як подавати котлети?", reply_markup=keyboard)


@router.message(Text(startswith="З"))
async def cmd_start1(message: types.Message):
     await message.reply("ЗБС")


@router.message(Text(startswith="Без"))
async def cmd_start2(message: types.Message):
     await message.reply("Так не смачно")


@router.message(Command("reply_builder"))
async def reply_builder(message: types.Message, command: CommandObject):
    num = int(command.args)
    print(f"{num=}")
    builder = ReplyKeyboardBuilder()
    builder.add(
        types.KeyboardButton(text="USD"),
        types.KeyboardButton(text="EUR"),
        types.KeyboardButton(text="KRN"),
        types.KeyboardButton(text="ZLT"),
        types.KeyboardButton(text="GBP"),
        types.KeyboardButton(text="YPI"),
        types.KeyboardButton(text="BTC"),
        types.KeyboardButton(text="ETH"),
    )
    builder.adjust(3, 2)
    await message.answer(
        "Виберіть число:",
        reply_markup=builder.as_markup(resize_keyboard=False, one_time_keyboard=True),
    )


DATA_DICT = {
    "USD": {
        "EUR": 0.9,
        "KRN": 13.03,
        "ZLT": 13.03,
        "GBP": 13.03,
        "YPI": 13.03,
    },
    "EUR": {
        "USD": 1.1,
        "KRN": 13.03,
        "ZLT": 13.03,
        "GBP": 13.03,
        "YPI": 13.03,
    },
    "KRN": {},
    "ZLT": {},
    "GBP": {},
    "YPI": {}
}


DATA_LIST = [
    {"currency": ("USD", "UAH"), "val": 45.03},
    {"currency": ("USD", "EUR"), "val": 0.9},
    {"currency": ("USD", "GBP"), "val": 0.8},
    {"currency": ("USD", "ZLT"), "val": 5.7},
    {"currency": ("UAH", "YPI"), "val": 12.0},
]


async def main() -> None:
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

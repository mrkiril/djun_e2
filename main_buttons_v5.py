import os

import logging
import asyncio
import sqlite3

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command, CommandObject, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
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

#
con = sqlite3.connect(config.db_name)
cursor = con.cursor()


class CurrencyState(StatesGroup):
    first_select = State()
    second_select = State()

# await state.set_state(CurrencyState.first_select)


def create_table():
    text = """
        CREATE TABLE IF NOT EXISTS currency (
            id integer PRIMARY KEY,
            from_currency TEXT NOT NULL,
            to_currency TEXT NOT NULL,
            value INTEGER,
            created_at TEXT,
            UNIQUE(from_currency,to_currency)
        );
    """
    response = cursor.execute(text)


def clear_table():
    text = "DELETE FROM currency;"
    response = cursor.execute(text)
    con.commit()


def insert_currency(curr_from: str, curr_to: str, value: float):
    # TODO: use cur.executemany("INSERT INTO movie VALUES(?, ?, ?)", data)
    text = f"""
        INSERT INTO currency (from_currency, to_currency, value, created_at)
        VALUES ('{curr_from}', '{curr_to}', {value}, datetime('now'));
    """
    response = cursor.execute(text)
    con.commit()


def add_currency_data():
    insert_currency("USD", "UAH", 36.6)
    insert_currency("USD", "EUR", 0.95)
    insert_currency("USD", "GBP", 0.86)


def get_unique_from_currency_data() -> list[str]:
    text = "select DISTINCT from_currency from currency;"
    response = cursor.execute(text)
    data = response.fetchall()  # [("USD",), ("EUR",)]
    return [uniq_curr[0] for uniq_curr in data]  # ["USD", "EUR", ...]


@router.message(Command("start"))
async def first_keyboard(message: types.Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()

    for curr_from in get_unique_from_currency_data():
        builder.add(types.KeyboardButton(text=curr_from))

    builder.adjust(4)
    await message.answer(
        "Виберіть валюту:",
        reply_markup=builder.as_markup(resize_keyboard=False, one_time_keyboard=True),
    )
    await state.set_state(CurrencyState.first_select)


@router.message(CurrencyState.first_select)
async def second_keyboard(message: types.Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    from_currency = message.text
    for to_currency_tuple in cursor.execute(f"select to_currency from currency where from_currency = '{message.text}';"):
        # [("EUR"), ("UAH",), ...]
        to_currency = to_currency_tuple[0]
        builder.add(types.KeyboardButton(text=f"{from_currency} -> {to_currency}"))

    builder.adjust(4)
    await message.answer(
        "Виберіть валюту для конвертації:",
        reply_markup=builder.as_markup(resize_keyboard=False, one_time_keyboard=True),
    )
    await state.set_state(CurrencyState.second_select)


# @router.message(F.text)
# async def second_keyboard(message: types.Message):
#     builder = ReplyKeyboardBuilder()
#
#     if "->" in message.text:
#         # message.text = "USD -> UAH"
#         from_currency, to_currency = message.text.split(" -> ")
#         resp = cursor.execute(f"select value from currency where from_currency = '{from_currency}' and to_currency = '{to_currency}';")
#         value = resp.fetchone()
#         await message.answer(f"Currency {message.text} = {value[0]}")
#         return
#
#     from_currency = message.text
#     for to_currency_tuple in cursor.execute(f"select to_currency from currency where from_currency = '{message.text}';"):
#         # [("EUR"), ("UAH",), ...]
#         to_currency = to_currency_tuple[0]
#         builder.add(types.KeyboardButton(text=f"{from_currency} -> {to_currency}"))
#
#     builder.adjust(4)
#     await message.answer(
#         "Виберіть валюту для конвертації:",
#         reply_markup=builder.as_markup(resize_keyboard=False, one_time_keyboard=True),
#     )


async def main() -> None:
    # ... and all other routers should be attached to Dispatcher
    create_table()
    clear_table()
    add_currency_data()
    dp.include_router(router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    # ;'; DELETE FROM currency;select '1
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

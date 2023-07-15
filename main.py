import os

import logging
import asyncio
import time

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, URLInputFile
from aiogram import html

from aiogram import F

from settings import config

logger = logging.getLogger(__name__)
# Bot token can be obtained via https://t.me/BotFahter


# Dispatcher is a root router
dp = Dispatcher()

# All handlers should be attached to the Router (or Dispatcher)
router = Router()


def user_name(message: Message):
    return html.quote(message.from_user.full_name)  #


@router.message(Command(commands=["start1"]))
async def command_start_handler1(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    await message.answer(f"Hello, <b>{message.from_user.full_name}!</b>")


@router.message(Command(commands=["start2"]))
async def command_start_handler2(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    await message.reply(f"Hello, <b>{message.from_user.full_name}!</b>")


@router.message(Command("pretty"))
async def any_message(message: types.Message):
    await message.answer("Hello, <b>world</b> <i>whole</i> <u>lalalala</u>!", parse_mode="HTML")


@router.message(Command("no-pretty"))
async def any_message(message: types.Message):
    await message.answer("Сообщение без <s>какой-либо разметки</s>", parse_mode=None)


@router.message(Command("fuck"))
async def any_message(message: types.Message):
    await message.reply(f"Hello, {html.bold(html.italic(user_name(message)))}!", parse_mode="HTML")


@router.message(Command("random_image"))
async def get_random_image(message: types.Message) -> None:
    """
    /random_image 500 600
    /random_image 500 -> Required 2 params but 1 given
    /random_image 500 500 500-> Required 2 params but 3 given
    /random_image -> Required 2 params but 0 given
    :param message:
    :return:
    """
    # Отправка файла по ссылке
    start_time = time.time()
    image_from_url = URLInputFile("https://picsum.photos/seed/groosha/400/300")
    result = await message.answer_photo(
        image_from_url,
        caption="Зображення по лінку"
    )
    await message.answer(f"Load image time is {round(time.time() - start_time, 2)}s")

#
# # TODO: Homework add more pretty tags here
#
@router.message(Command("dice"))
async def cmd_dice(message: types.Message):
    """
    :param emoji: Emoji on which the dice throw animation is based.
    Currently, must be one of '🎲', '🎯', '🏀', '⚽', '🎳', or '🎰'.
    Dice can have values 1-6 for '🎲', '🎯' and '🎳',
                  values 1-5 for '🏀' and '⚽', and
                  values 1-64 for '🎰'.
                  Defaults to '🎲'
    :param message:
    :return:
    """
    await message.answer_dice(emoji="🎰")


from aiogram.enums.dice_emoji import DiceEmoji
#
@router.message(Command("dice2"))
async def cmd_dice(message: types.Message):
    """
    :param emoji: Emoji on which the dice throw animation is based.
    Currently, must be one of '🎲', '🎯', '🏀', '⚽', '🎳', or '🎰'.
    Dice can have values 1-6 for '🎲', '🎯' and '🎳',
                  values 1-5 for '🏀' and '⚽', and
                  values 1-64 for '🎰'.
                  Defaults to '🎲'
    :param message:
    :return:
    """
    await message.answer_dice(emoji=DiceEmoji.DART)


@router.message(Command("name"))
async def cmd_name(message: types.Message, command: CommandObject):
    """
    command.args -> nora -> Hello NY
    command.args -> nono -> Hello LA
    command.args -> nana -> Hello LA
    command.args -> tttt -> Hello IOWA
    :param message:
    :param command:
    :return:
    """
    name = html.quote(command.args)
    await message.answer(f"Hello, NY -> {command.args.split()}")

# # we can use
# # F.text
# # F.animation
# # F.photo
# # F.sticker
# # F.video
# # F.new_chat_members
#

@router.message(F.text)
async def echo_handler(message: types.Message) -> None:
    try:
        await message.reply("F.text reply")
    except TypeError:
        await message.answer("Nice try!")


@router.message(F.photo)
async def echo_handler(message: types.Message) -> None:
    try:
        await message.reply("F.photo reply")
    except TypeError:
        await message.answer("Nice try!")


@router.message(F.video)
async def echo_handler(message: types.Message) -> None:
    try:
        await message.reply("F.video reply")
    except TypeError:
        await message.answer("Nice try!")


@router.message(F.animation)
async def echo_handler(message: types.Message) -> None:
    try:
        await message.reply("F.animation reply")
    except TypeError:
        await message.answer("Nice try!")


@router.message(F.sticker)
async def echo_handler(message: types.Message) -> None:
    try:
        await message.reply("F.sticker reply")
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

from settings import config


print(f"BOT_TOKEN -> {config.bot_token.get_secret_value()}")
print(f"CAR_NUMBER -> {config.card_number}")

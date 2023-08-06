import os
from pantrypal import Recipe
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


class TelegramBot:
    def __init__(self) -> None:
        # Construct Telegram bot
        self.updater = Updater(os.environ["TG_API_KEY"], use_context=True)
        dp = self.updater.dispatcher

        # Commands
        dp.add_handler(CommandHandler("start", self._start_command))
        dp.add_handler(CommandHandler("help", self._help_command))
        dp.add_handler(CommandHandler("cancel", self._cancel_command))
        dp.add_handler(CommandHandler("addrecipe", self._add_recipe))

        # Messages
        dp.add_handler(MessageHandler(Filters.text, self._process_message))

        # Log all errors
        dp.add_error_handler(self._error_handler)

        # Run bot
        self.updater.start_polling()
        self.updater.idle()

    def _start_command(self, update, context):
        """PantryPal Telegram bot start command handler."""
        update.message.reply_text(
            "Welcome to PantryPal! Have a look "
            + "at the commands below to get started."
        )

    def _help_command(self, update, context):
        """PantryPal Telegram bot help command handler."""
        update.message.reply_text("Help will be added soon.")

    def _cancel_command(self, update, context):
        """PantryPal Telegram bot cancel command handler."""
        update.message.reply_text("Cancel command will be added soon.")

    def _process_message(self, update, context):
        """PantryPal Telegram bot message handler."""
        update.message.reply_text("I'm not ready to handle that yet...")

    def _error_handler(self, update, context):
        """PantryPal Telegram bot error handler."""
        update.message.reply_text("Oops - something wen't wrong.")

    def _add_recipe(self, update, context):
        """Add recipe."""
        message = str(update.message.text).lower()
        recipe = Recipe.from_url(message)
        update.message.reply_text(f"Added '{recipe}'.")


if __name__ == "__main__":
    TelegramBot()

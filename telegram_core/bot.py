from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

from telegram_core import responder

updater = Updater("1874452082:AAG6JqHB704XuIbMdLF8lKOBHvJncNB3C0w")

updater.dispatcher.add_handler(CommandHandler('start', responder.start, Filters.chat_type.private))
updater.dispatcher.add_handler(MessageHandler(Filters.photo & Filters.chat_type.private,
                                              responder.handle_image_as_picture))
updater.dispatcher.add_handler(MessageHandler(Filters.document & Filters.chat_type.private,
                                              responder.handle_image_as_document))

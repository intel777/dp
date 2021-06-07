import os

from telegram_core.bot import updater


if __name__ == '__main__':
    if not os.path.exists('temp'):
        os.makedirs('temp')

    updater.start_polling()
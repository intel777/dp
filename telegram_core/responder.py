import os

from analyzer import analyze_and_respond


def start(update, context):
    print(f'[telegram_core][responder]Handling start command from: {update.effective_user.id}')
    update.message.reply_text('Вітаю! Для отримання інформації відправте зображення. Бажано документом.')


def handle_image_as_picture(update, context):
    print(f'[telegram_core][responder]Handling image from user: {update.effective_user}')
    photo = update.message.photo[-1].get_file()
    image_path = f'temp/{photo.file_path.split("/")[-1]}'
    photo.download(image_path)
    analyze_and_respond(image_path, update)
    os.remove(image_path)


def handle_image_as_document(update, context):
    print(f'[telegram_core][responder]Handling document from user: {update.effective_user}')
    document = update.message.document.get_file()
    if document.file_path.split('/')[-1].split('.')[-1].lower() in ('jpg', 'jpeg'):
        image_path = f'temp/{document.file_path.split("/")[-1]}'
        document.download(image_path)
        analyze_and_respond(image_path, update)
        os.remove(image_path)
    else:
        update.message.reply_text('Unsupported format!')

import json


def get_content(item, bot, CHANNEL_NAME):
    photo = item.get('attachments', '')[0].get('photo', '').get('photo_807', '')
    bot.send_photo(CHANNEL_NAME, photo)
def save(di: dict, arg= 'w', path='save.json') -> None:
    with open(path, arg) as js:  # or 'w'
        js.write(json.dumps(di, indent=4) + ',\n')
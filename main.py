from Autopost import Posting

URL_VK = "https://api.vk.com/method/wall.get"
TOKEN = ""  # your token
BOT_TOKEN = ''  # token bot

CHANNEL_NAME = '@name'  # @my_channel_name
BASE_POST_URL = 'https://vk.com/wall-163703907_'
DOMAIN = "haccking1"

VERSION = 5.68
FILENAME_VK = 'path.txt'  # id post
SINGLE_RUN = True  # depending on the value of SINGLE_RUN, it will either work constantly, checking every 4 minutes


# for new posts, or will end after the first check
def get_content(item, bot, CHANNEL_NAME):
    try:
        link = item.get('attachments', '')[0].get('link', '').get('url', '')
        bot.send_message(CHANNEL_NAME, f" [#READ]({link})", parse_mode='markdown')

    except IOError as e:
        pass
    # bot.send_photo(CHANNEL_NAME, photo)
    finally:
        try:
            photo = item.get('attachments', '')[0].get('photo', '').get('photo_604', '')
            bot.send_photo(CHANNEL_NAME, photo)

        except IOError as e:
            pass


tb = Posting(FILENAME_VK, URL_VK, TOKEN, BOT_TOKEN, CHANNEL_NAME, BASE_POST_URL, DOMAIN, VERSION, SINGLE_RUN,
             get_content)
tb.main()

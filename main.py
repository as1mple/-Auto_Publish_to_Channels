from Autopost import Autopost

URL_VK = "https://api.vk.com/method/wall.get"
TOKEN = ""  # vk_token
BOT_TOKEN = ''  # token bot

CHANNEL_NAME = '@temparary'  # @my_channel_name
BASE_POST_URL = 'https://vk.com/wall-61560900_'
DOMAIN = "minimalism"

VERSION = 5.68
FILENAME_VK = 'last_known_id.txt'
SINGLE_RUN = True  # depending on the value of SINGLE_RUN, it will either work constantly, checking every 4 minutes
# for new posts, or will end after the first check

tb = Autopost(FILENAME_VK, URL_VK, TOKEN, BOT_TOKEN, CHANNEL_NAME, BASE_POST_URL, DOMAIN, VERSION, SINGLE_RUN)
tb.main()

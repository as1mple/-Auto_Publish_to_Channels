import time
from tools import save

import logging
import telebot
import eventlet
import requests


class Posting:
    def __init__(self, FILENAME_VK, URL_VK, TOKEN, BOT_TOKEN, CHANNEL_NAME, BASE_POST_URL, DOMAIN, VERSION, SINGLE_RUN,
                 GET_CONTENT):
        self.FILENAME_VK = FILENAME_VK
        self.URL_VK = URL_VK
        self.TOKEN = TOKEN
        self.BOT_TOKEN = BOT_TOKEN
        self.bot = telebot.TeleBot(self.BOT_TOKEN)
        self.CHANNEL_NAME = CHANNEL_NAME
        self.BASE_POST_URL = BASE_POST_URL
        self.DOMAIN = DOMAIN
        self.VERSION = VERSION
        self.SINGLE_RUN = SINGLE_RUN
        self.GET_CONTENT = GET_CONTENT

    def get_data(self) -> dict or None:
        timeout = eventlet.Timeout(10)
        try:
            response = requests.get(self.URL_VK,
                                    params={
                                        "domain": self.DOMAIN,
                                        "count": "5",  # <100
                                        "access_token": self.TOKEN,
                                        "v": self.VERSION,
                                    },
                                    proxies={"https": "188.191.165.92:8080"}
                                    )
            data = response.json()
            logging.info(data)
            logging.info("finish scanning")
            save(data)
            return data
        except eventlet.timeout.Timeout:
            logging.warning('Got Timeout while retrieving VK JSON data. Cancelling...')
            return None
        finally:
            timeout.cancel()

    def send_new_posts(self, items, last_id):
        logging.info("start send")
        for item in items:
            try:
                if item['id'] <= last_id:
                    logging.info("repeat")
                    print(item['id'] <= last_id)
                    break
                self.GET_CONTENT(item, self.bot, self.CHANNEL_NAME)
                # We sleep a second to avoid all sorts of errors and restrictions (just in case!)
                time.sleep(1)
            except Exception as e:
                logging.error('Exception of type {!s} in check_new_post(): {!s}'.format(type(e).__name__, str(e)))
        return

    def check_new_posts_vk(self) -> None:
        logging.info('[VK] Started scanning for new posts')  # start time
        with open(self.FILENAME_VK, 'rt') as file:
            last_id = int(file.read())
            print(last_id)
            if last_id is None:
                logging.error('Could not read from storage. Skipped iteration.')
                return
            logging.info('Last ID (VK) = {!s}'.format(last_id))
        try:
            print("wait...")
            feed = self.get_data()
            # If a timeout occurred earlier, skip the iteration. If everything is fine - parse posts.
            if feed is not None:
                entries = feed.get('response', '').get('items', '')[1:]
                try:
                    # If the post has been fixed, skip it
                    # And start sending messages
                    self.send_new_posts(entries[1:], last_id)
                except KeyError:
                    self.send_new_posts(entries, last_id)
                # Write the new last_id to the file.
                with open(self.FILENAME_VK, 'wt') as file:
                    try:
                        # If the first post is fixed, then we save the ID of the second
                        file.write(str(entries[1]['id']))
                        logging.info('New last_id (VK) is {!s}'.format((entries[1]['id'])))
                    except KeyError:
                        file.write(str(entries[0]['id']))
                        logging.info('New last_id (VK) is {!s}'.format((entries[0]['id'])))
        except KeyError as ex:
            logging.error('Exception of type {!s} in check_new_post(): {!s}'.format(type(ex).__name__, str(ex)))
            pass
        logging.info('[VK] Finished scanning')
        return

    def main(self):
        # We get rid of spam in logs from the request library
        logging.getLogger('requests').setLevel(logging.CRITICAL)
        # Configure our logger
        logging.basicConfig(format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s',
                            level=logging.INFO,
                            filename='bot_log.log', datefmt='%d.%m.%Y %H:%M:%S')
        if not self.SINGLE_RUN:
            while True:
                self.check_new_posts_vk()
                # 4 minutes pause before re-checking
                logging.info('[App] Script went to sleep.')
                time.sleep(60 * 4)
        else:
            self.check_new_posts_vk()
        logging.info('[App] Script exited.\n')

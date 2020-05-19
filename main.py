from database.connector import Database
from database.message import log_message
import markov.process as markov
from dotenv import load_dotenv
import discord
import os

class MyClient(discord.Client):
    async def on_ready(self):
        self.database = Database()
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

        cur = self.database.cur()
        log_message(cur, message)
        if message.type == discord.MessageType.default:
            markov.process_message(cur, message.id, message.content)
            print('handled message')
        cur.close()

if __name__ == '__main__':
    load_dotenv()
    client = MyClient()
    client.run(os.getenv('BOT_TOKEN'))

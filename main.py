import discord
from dotenv import load_dotenv
from database.connector import Database
import os

class MyClient(discord.Client):
    async def on_ready(self):
        self.database = Database()
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

if __name__ == '__main__':
    load_dotenv()
    client = MyClient()
    client.run(os.getenv('BOT_TOKEN'))

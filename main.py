from database.connector import Database
from database.message import insert_message
import markov.generator as generator
import markov.process as process
from loader.loader import load_server_messages, get_word_count
from dotenv import load_dotenv
import discord
import os

class MyClient(discord.Client):
    async def on_ready(self):
        self.database = Database()
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

        if message.author.id == client.user.id or message.author.bot:
            return

        cur = self.database.cur()
        if message.content.lower().startswith("$load-markov"):
            message_count = await load_server_messages(cur, message.guild)
            await self.get_channel(message.channel.id).send(f"Loaded {message_count} messages")
        elif message.content.lower().startswith("bot be random"):
            markov_message = generator.generate_message(cur, message.guild.id)
            if markov_message is None:
                await self.get_channel(message.channel.id).send("Failed to generate a message")
            else:
                await self.get_channel(message.channel.id).send(markov_message)
        else:
            if message.type == discord.MessageType.default:
                word_count = get_word_count(message.content)
                insert_message(cur, message, word_count)
                process.process_message(cur, message)
                print('loaded')
        cur.close()

if __name__ == '__main__':
    load_dotenv()
    client = MyClient()
    client.run(os.getenv('BOT_TOKEN'))

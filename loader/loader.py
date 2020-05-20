from database.loader import channel_loaded, mark_channel_loaded
from database.message import insert_message
from markov.process import process_message, clean_word
import discord

async def load_server_messages(cur, client_user_id, server):
    message_count = 0

    client = discord.utils.find(lambda m: m.id == client_user_id, server.members)
    if client is None:
        print("couldn't find client")
        return

    cur.execute("BEGIN")
    for channel in filter(lambda c: c.type == discord.ChannelType.text, server.channels):
        if channel_loaded(cur, channel.id) or not channel.permissions_for(client).read_message_history:
            continue

        message_count += await load_channel(cur, channel, 6000)
        mark_channel_loaded(cur, channel.id)
    cur.execute("COMMIT")
    return message_count

async def load_channel(cur, channel, message_count):
    messages = await get_messages(channel, message_count)
    for message in messages:
        word_count = get_word_count(message.content)
        insert_message(cur, message, word_count)
        process_message(cur, message)
    return len(messages)
    
async def get_messages(channel, message_count):
    count = 0
    before = None
    loaded_messages = []
    while count < message_count:
        print(count)
        hasMessages = False
        async for message in channel.history(limit=500, before=before):
            if message.author.bot:
                continue

            hasMessages = True
            if before is None or message.id < before.id:
                before = message

            loaded_messages.append(message)
            count += 1
        if not hasMessages:
            break
    return loaded_messages

def get_word_count(message):
    words = message.split(' ')
    words = filter(lambda w: len(w) > 0, map(lambda w: clean_word(w), words))
    return len(list(words))

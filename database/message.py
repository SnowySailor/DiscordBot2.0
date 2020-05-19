def insert_message(cur, message, word_count):
    query = "INSERT INTO message (id, channel_id, server_id, data, word_count) values (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"
    cur.execute(query, [message.id, message.channel.id, message.guild.id, message.content, word_count])

def log_message(cur, message):
    query = "INSERT INTO message (id, channel_id, server_id, data) values (%s, %s, %s, %s)"
    cur.execute(query, [message.id, message.channel.id, message.guild.id, message.content])

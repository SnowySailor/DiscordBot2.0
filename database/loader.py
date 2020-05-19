def channel_loaded(cur, channel_id):
    query = "SELECT * FROM loaded_channel WHERE channel_id = %s"
    cur.execute(query, [channel_id])
    if cur.fetchone() is None:
        return False
    return True

def mark_channel_loaded(cur, channel_id):
    query = "INSERT INTO loaded_channel (channel_id) VALUES (%s)"
    cur.execute(query, [channel_id])

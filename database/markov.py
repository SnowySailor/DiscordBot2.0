def get_random_message(cur, server_id):
    query = """
        SELECT digested_text, original_text FROM markov_grouping mg
        WHERE
            message_id = (
                SELECT message_id FROM messages
                WHERE server_id = %s
                ORDER BY RANDOM()
                LIMIT 1
            )
            AND
            not exists(
                SELECT * FROM message m
                WHERE
                    mg.message_id = m.id
                    AND
                    m.deleted = true
            )
    """
    rows = cur.execute(query, [server_id])
    if len(rows) == 1:
        return (rows[0][0], rows[0][1])
    return None

def get_random_prefixed_message(cur, server_id, prefix):
    query = """
        SELECT * FROM markov_grouping mg
        WHERE
            server_id = %s
            AND
            digested_text LIKE '%s%'
            AND
            not exists(
                SELECT * FROM message m
                WHERE
                    mg.message_id = m.id
                    AND
                    m.deleted = true
            )
        ORDER BY RANDOM()
        LIMIT 1
    """
    rows = cur.execute(cur, [server_id, prefix])
    if len(rows) == 1:
        return (rows[0][1], rows[0][2])
    return None

def insert_markov_grouping(cur, message_id, digested_text, original_text):
    query = "INSERT INTO markov_grouping (message_id, digested_text, original_text) VALUES (%s, %s, %s)"
    cur.execute(query, [message_id, digested_text, original_text])

def insert_message(cur, id, channel_id, message_id, data):
    query = "INSERT INTO message (id, channel_id, message_id, data) VALUES (%s, %s, %s, %s)"
    cur.execute(query, [id, channel_id, message_id, data])

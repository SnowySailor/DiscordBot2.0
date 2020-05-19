def get_random_message(cur, server_id, min_word_count = 5):
    query = """
        SELECT digested_text, original_text FROM markov_grouping mg
        WHERE
            message_id = (
                SELECT id FROM message
                WHERE
                    server_id = %s
                    AND
                    digested = true
                    AND
                    word_count > %s
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
        ORDER BY RANDOM()
        LIMIT 1
    """
    cur.execute(query, [server_id, min_word_count])
    row = cur.fetchone()
    if row is not None:
        return (row[0], row[1])
    return None

def get_random_prefixed_message(cur, server_id, prefix, min_word_count = 5):
    query = """
        SELECT digested_text, original_text FROM markov_grouping mg
        INNER JOIN message m ON mg.message_id = m.id
        WHERE
            m.server_id = %s
            AND
            digested_text LIKE CONCAT(%s, '%%')
            AND
            m.deleted = false
            AND
            m.digested = true
            AND
            m.word_count > %s
        ORDER BY RANDOM()
        LIMIT 1
    """
    cur.execute(query, [server_id, prefix, min_word_count])
    row = cur.fetchone()
    if row is not None:
        return (row[0], row[1])
    return None

def insert_markov_grouping(cur, message_id, digested_text, original_text):
    query = "INSERT INTO markov_grouping (message_id, digested_text, original_text) VALUES (%s, %s, %s)"
    cur.execute(query, [message_id, digested_text, original_text])

def mark_message_digested(cur, message_id):
    query = "UPDATE message SET digested = true WHERE id = %s"
    cur.execute(query, [message_id])

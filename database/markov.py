def get_random_seed_message(cur, server_id, min_word_count = 5):
    query = """
        SELECT digested_text, original_text FROM markov_grouping mg
        INNER JOIN message m ON m.id = mg.message_id
        WHERE
            m.server_id = %s
            AND
            m.digested = true
            AND
            m.word_count > %s
            AND
            m.deleted = false
            AND
            mg.is_message_start = true
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

def insert_markov_grouping(cur, message_id, digested_text, original_text, is_message_start):
    query = "INSERT INTO markov_grouping (message_id, digested_text, original_text, is_message_start) VALUES (%s, %s, %s, %s)"
    cur.execute(query, [message_id, digested_text, original_text, is_message_start])

def mark_message_digested(cur, message_id):
    query = "UPDATE message SET digested = true WHERE id = %s"
    cur.execute(query, [message_id])

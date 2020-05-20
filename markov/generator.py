from database.markov import get_random_seed_message, get_random_prefixed_message

def generate_message(cur, server_id):
    seed = get_random_seed_message(cur, server_id)
    if seed is not None:
        (seed_digested, seed_original) = seed
        next_prefix = get_next_digest_prefix(seed_digested)
        if next_prefix is None:
            print('fail 1')
            return None
    else:
        print('fail 3')
        return None

    message = seed_original
    while len(message) < 300:
        seed = get_random_prefixed_message(cur, server_id, next_prefix)
        if seed is not None:
            (seed_digested, seed_original) = seed
            next_prefix = get_next_digest_prefix(seed_digested)
            if next_prefix is None:
                print('fail 2')
                return None
        else:
            break
        message += ' ' + get_last_word(seed_original)

    return message

def get_last_word(message):
    return message.split(' ')[-1]

def get_last_two_words(message):
    return message.split(' ')[-1]

def get_all_but_last_word(message):
    return ' '.join(message.split(' ')[:-1])

def get_all_but_last_two_words(message):
    return ' '.join(message.split(' ')[:-2])

def get_next_digest_prefix(digested):
    try:
        idx = digested.index(':')
        return digested[idx + 1:] + ':'
    except:
        return None

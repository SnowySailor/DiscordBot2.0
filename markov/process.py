from database.markov import get_random_message, get_random_prefixed_message
import re

def process_message(cur, message):
    triples = generate_triples(message.split(' '))

    markov_messages = []
    for triple in triples:
        digest = generate_digest(triple)
        if digest is None:
            continue

        original = generate_original(triple)
        markov_messages.append((message_id, digest, original))

def generate_message(cur, server_id):
    seed = get_random_message(cur, server_id)
    if seed is not None:
        (seed_digested, seed_original) = seed
        next_prefix = get_next_digest_prefix(seed_digested)
        if next_prefix is None:
            return None
    else:
        return None

    message = seed_original
    while len(message) < 100:
        seed = get_random_prefixed_message(cur, server_id, next_prefix)
        if seed is not None:
            (seed_digested, seed_original) = seed
            next_prefix = get_next_digest_prefix(seed_digested)
            if next_prefix is None:
                return None
        else:
            break
        message += ' ' + seed_original

    return message

def get_next_digest_prefix(digested):
    try:
        idx = digested.index(':')
        return digested[idx + 1:] + ':'
    except:
        return None

def generate_triples(words):
    if len(words < 3):
        return []

    triples = []
    for i in range(len(words) - 2):
        triples.append((words[i], words[i+1], words[i+2]))
    return triples

def generate_digest(triple):
    digests = []
    for word in triple:
        digest = re.sub('[\'\[\]@#$^&*\\\{\}`~<>+=\-_/|:]', '', word).lower()
        if digest == '':
            return None
        digests.append(digest)
    return ':'.join(digest)

def generate_original(triple):
    return triple.join(' ')

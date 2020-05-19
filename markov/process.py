from database.markov import insert_markov_grouping
import re

def process_message(cur, message_id, message):
    triples = generate_triples(message.split(' '))

    for triple in triples:
        digest = generate_digest(triple)
        if digest is None:
            continue
        original = generate_original(triple)

        insert_markov_grouping(cur, message_id, digest, original)

def generate_triples(words):
    if len(words) < 3:
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
    return ':'.join(digests)

def generate_original(triple):
    return ' '.join(triple)

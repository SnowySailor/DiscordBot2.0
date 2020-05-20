from database.markov import insert_markov_grouping
from database.markov import mark_message_digested
import re

def process_message(cur, message):
    triples = generate_triples(message.content.split(' '))

    message_marked_digested = False
    is_message_start = True
    for triple in triples:
        digest = generate_digest(triple)
        if digest is None:
            continue
        original = generate_original(triple)

        insert_markov_grouping(cur, message.id, digest, original, is_message_start)
        if not message_marked_digested:
            mark_message_digested(cur, message.id)
            message_marked_digested = True
            is_message_start = False

def generate_triples(words):
    if len(words) < 3:
        return []

    triples = []
    for i in range(len(words) - 2):
        triples.append((words[i], words[i+1], words[i+2]))
    return triples

def generate_quadruples(words):
    if len(words) < 4:
        return []

    triples = []
    for i in range(len(words) - 3):
        triples.append((words[i], words[i+1], words[i+2], words[i+3]))
    return triples

def generate_digest(words):
    digests = []
    for word in words:
        digest = clean_word(word)
        if digest == '':
            return None
        digests.append(digest)
    return ':'.join(digests)

def clean_word(word):
    return re.sub('[\'\[\]@#$^&*\\\{\}`~<>+=\-_/|:]', '', word).lower()

def generate_original(triple):
    return ' '.join(triple)

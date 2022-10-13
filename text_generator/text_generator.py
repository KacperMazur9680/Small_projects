from collections import Counter
import nltk
# nltk.download()
import random

FILENAME = "./text_generator/data/corpus.txt"


with open(FILENAME, "r", encoding="utf-8") as f:
    content = f.read()

tokens = nltk.regexp_tokenize(content, r"[^\s]+")
bigrams = list(nltk.bigrams(tokens))

head_tails = {}
for head, tail in bigrams:
    head_tails.setdefault(head, []).append(tail)

words_in_sentence = 10
sentences = 10
for s in range(sentences):
    text = ""
    head = random.choice(list(head_tails.keys()))
    for w in range(words_in_sentence):
        reps = dict(Counter(head_tails[head]))

        most_propable = []

        for key, value in reps.items():
            if value == max(list(reps.values())):
                most_propable.append(key)

        head = random.choice(most_propable)
        text += f"{head} "
    
    print(text)
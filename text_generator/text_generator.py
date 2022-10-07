from collections import Counter
import nltk
# nltk.download()

FILENAME = "./text_generator/data/corpus.txt"

with open(FILENAME, "r", encoding="utf-8") as f:
    content = f.read()

tokens = nltk.regexp_tokenize(content, r"[^\s]+")
bigrams = list(nltk.bigrams(tokens))

head_tails = {}
for head, tail in bigrams:
    head_tails.setdefault(head, []).append(tail)

while True:
    head = input()
    if head == "exit":
        break
    try:
        reps = dict(Counter(head_tails[head]))
    except TypeError:
            print("Type Error. Please input a string.")
    except KeyError:
            print("Key Error. The requested word is not in the model. Please input another word.")
    except ValueError:
            print("Value error. Please input a string.")
    else:
        print(f"Head: {head}")
        for word, rep in reps.items():
            print(f"Tail: {word}\tCount: {rep}")

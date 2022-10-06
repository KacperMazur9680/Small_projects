import nltk
# nltk.download()

FILENAME = "./text_generator/data/corpus.txt"

with open(FILENAME, "r", encoding="utf-8") as f:
    content = f.read()

tokens = nltk.regexp_tokenize(content, r"[^\s]+")
bigrams = list(nltk.bigrams(tokens))

print(f"Number of bigrams: {len(bigrams)}")
print()

while True:
    word = input()
    if word == "exit":
        break
    try:
        word_index = int(word)
        if word_index == -1:
            print(f"Head: {tokens[word_index - 1]}\tTail: {tokens[word_index]}")
        else:
            print(f"Head: {tokens[word_index]}\tTail: {tokens[word_index + 1]}")
    except TypeError:
            print("Type Error. Please input an integer.")
    except IndexError:
            print("Index Error. Please input an integer that is in the range of the corpus.")
    except ValueError:
            print("Value error. Please input an integer.")
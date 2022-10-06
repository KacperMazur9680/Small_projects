# import nltk
# nltk.download()

FILENAME = "./text_generator/data/corpus.txt"

with open(FILENAME, "r", encoding="utf-8") as f:
    content = f.read()

tokens = content.split()

print(f"Corpus statistics\nAll tokens: {len(tokens)}\nUnique tokens: {len(set(tokens))}")
print()

while True:
    word = input()
    if word == "q":
        break

    try:
        word_index = int(word)
        print(tokens[word_index])
    except TypeError:
            print("Type Error. Please input an integer.")
    except IndexError:
            print("Index Error. Please input an integer that is in the range of the corpus.")
    except ValueError:
            print("Value error. Please input an integer.")
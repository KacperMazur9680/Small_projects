from collections import Counter
import nltk
# nltk.download()
import random


class Words_Generator:
    def __init__(self, filename):
        self.filename = filename
        self.punc = "?!."
        self.head_tails = dict()
    
    def tokenize(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            content = f.read()
        self.tokens = nltk.regexp_tokenize(content, r"[^\s]+")

        return self.tokens

    def get_trigram(self):
        self.trigrams = list(nltk.trigrams(self.tokens))
        return self.trigrams

    def get_head_tail(self):
        for head1, head2, tail in self.trigrams:
            head = f"{head1} {head2}"
            self.head_tails.setdefault(head, []).append(tail)

        return self.head_tails

    def generate_sentences(self, sentences, min_words):
        min_words -= 2
        def predict_words(head):
            reps = dict(Counter(self.head_tails[head]))
            most_propable = []

            for key, value in reps.items():
                if value == max(list(reps.values())):
                    most_propable.append(key)

            self.head = head.split()[1] + " " + random.choice(most_propable)
            self.text += f"{self.head.split()[1]} "
            return self.text

        for s in range(sentences):
            self.text = ""
            w = 0
            while True:
                self.head = random.choice(list(self.head_tails.keys()))
                sub_head = self.head.split()
                if self.head[0].isupper() and sub_head[0][-1] not in self.punc:
                    self.text += f"{self.head} "
                    break
            
            while w < min_words:
                predict_words(self.head)
                w += 1
            
            if self.text[-2] not in self.punc:
                while True:
                    predict_words(self.head)
                    if self.text[-2] in self.punc:
                        break
        
            print(self.text)


if __name__ == "__main__":
    generator = Words_Generator("./text_generator/data/corpus.txt")
    generator.tokenize()
    generator.get_trigram()
    generator.get_head_tail()
    generator.generate_sentences(10, 5)
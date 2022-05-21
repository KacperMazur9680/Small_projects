import glob 

def preprocess_review(review):
    """Removing html extras and convert str into a list."""

    return review.lower().replace("<br />", " ").split()

def count_words(path_pattern):

    """Counting in how many files each word appeard, store the info in a dictionary."""

    words_count = {}
    files = glob.glob(path_pattern)
    for file in files:
        with open(file, encoding="utf-8") as stream:
            content = stream.read()
            words = preprocess_review(content)
            for word in set(words):
                words_count[word] = words_count.get(word, 0) + 1

    return words_count

def compute_sentiment(words, words_count_pos, words_count_neg, debug=False):

    """Calculating the comments sentiment.
    
    debug - if set True, show the sentiment of each word"""

    comment_sentiment = 0
    for word in words:
        positive = words_count_pos.get(word, 0)
        negative = words_count_neg.get(word, 0)
        all_ = positive + negative
        if all_ == 0:
            word_sentiment = 0
        else:
            word_sentiment = (positive - negative) / all_
        if debug:
            print(word, word_sentiment)
        
        comment_sentiment += word_sentiment
    comment_sentiment /= len(words)

    return comment_sentiment

def print_sentiment(sentiment):
    """Informing what kind of comment was added."""
    if sentiment > 0:
        label = "positive"
    else:
        label = "negative"
    print(f"This comment is {label}, its sentiment is equal {sentiment}.")

def main():
    words_count_pos = count_words("*/comment_evaluationer/comments/pos/*.txt")
    words_count_neg = count_words("*/comment_evaluationer/comments/neg/*.txt")

    comment = input("Enter your comment: ")
    words = preprocess_review(comment)
    sentiment = compute_sentiment(words, words_count_pos, words_count_neg, debug=True)

    print("------------------")
    print_sentiment(sentiment)

if __name__ == "__main__":
    main()
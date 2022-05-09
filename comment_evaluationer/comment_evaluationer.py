import glob 
POSITIVE = glob.glob("Small_projects/comment_evaluationer/comments/pos/*.txt")  # Path with the positive comments
NEGATIVE = glob.glob("Small_projects/comment_evaluationer/comments/neg/*.txt")  # Path with the negative comments
PUNCTUATION = "-+!@#$%^&*(),.?/"

# For each file in the pos/neg directory, replace html's "enter" and any punctuations with a space,
# make every word lowercase, convert every file to a list of words,
# convert made list to a set to avoid repetitions, add each word to the dictionary,
# Note: if said word is already in the dictionary its value is increaced by one
positive_dict = {}
for file in POSITIVE:
    with open(file, encoding="utf8") as stream:
        content = stream.read()

    content = content.replace("<br /><br />", " ")
    for punc in PUNCTUATION:
        content = content.replace(punc, " ")

    content = content.lower().split()
    for word in set(content):
        positive_dict[word] = positive_dict.get(word, 0) + 1

negative_dict = {}

for file in NEGATIVE:
    with open(file, encoding="utf8") as stream:
        content = stream.read()

    content = content.replace("<br /><br />", " ")
    for punc in PUNCTUATION:
        content = content.replace(punc, " ")

    content = content.lower().split()
    for word in set(content):
        negative_dict[word] = negative_dict.get(word, 0) + 1

# Prompt the user for a comment
new_comment = input("Enter your comment: ")
words = new_comment.lower().split()
sentiment_sum = 0

# Math behind each words sentiment
for word in words: 
    positive = positive_dict.get(word, 0)
    negative = negative_dict.get(word, 0)

    all_ = positive + negative
    if all_ != 0:
        word_sentiment = (positive-negative)/all_
    else:
        word_sentiment = 0.0
    print(word, word_sentiment)

    sentiment_sum += word_sentiment

sentiment = sentiment_sum/len(words)

# Informing what kind of comment was added
if sentiment > 0:
    label = "positive"
elif sentiment < 0:
    label = "negative"
else:
    label = "neutral"

print(f"The added comment is {label} and it has a {sentiment} sentiment.")

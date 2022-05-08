import glob
POSITIVE = glob.glob("Small_projects/comment_evaluationer/comments/pos/*.txt")
NEGATIVE = glob.glob("Small_projects/comment_evaluationer/comments/neg/*.txt")
PUNCTUATION = ",.?!@#$%^&()"

positive_comments = []
negative_comments = []

# for each file in the pos/neg directory, replace html's "enter" and any punctuations with space,
# make every word lower case and convert every file to a list that we append to an external list.
for file in POSITIVE:
    with open(file, encoding="utf8") as f:
        content = f.read()
    content = content.replace("<br />", " ")
    for punc in PUNCTUATION:
        content = content.replace(punc, " ")
    content = content.lower().split()
    positive_comments.append(content)

for file in NEGATIVE:
    with open(file, encoding="utf8") as f:
        content = f.read()
    content = content.replace("<br />", " ")
    for punc in PUNCTUATION:
        content = content.replace(punc, " ")
    content = content.lower().split()
    negative_comments.append(content)

# new comment prompt.
new_comment = input("Enter you comment: ")
words = new_comment.split()
sentiment_sum = 0

# going through every word.
for word in words:
    positive = 0  
    negative = 0  

# checking in how many listed comments (pos and neg) a certain word appeared.
    for comment in positive_comments:
        if word.lower() in comment:
            positive += 1

    for comment in negative_comments:
        if word.lower() in comment:
            negative += 1

# math behind each words sentiment.
    all_ = positive + negative
    if all_ != 0:
        word_sentiment = (positive-negative)/all_
    else:
        word_sentiment = 0.0
    print(word, word_sentiment)

    sentiment_sum += word_sentiment

sentiment = sentiment_sum/len(words)

# informing what kind of comment was added. 
if sentiment > 0:
    label = "positive"
elif sentiment < 0:
    label = "negative"
else:
    label = "neutral"

print(f"The sentense in {label} and it has a sentiment {sentiment}")
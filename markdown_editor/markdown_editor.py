FORMATTERS = ["plain", "bold", "italic", "header", "link", "inline-code", "ordered-list", "unordered-list", "new-line"]


def header():
    while True:
        lvl = int(input("Level: "))
        if lvl <= 0 or lvl > 6:
            print("The level should be within the range of 1 to 6")
        else:
            break

    text = input("Text: ")
    if len(f_texts) == 0:
        return "#" * lvl + " " + text + "\n"
    else:
        return "\n" + "#" * lvl + " " + text + "\n"

def plain():
    text = input("Text: ")
    return text

def bold():
    text = input("Text: ")
    return f"**{text}**"

def italic():
    text = input("Text: ")
    return f"*{text}*"

def inline():
    text = input("Text: ")
    return f"`{text}`"

def link():
    label = input("Label: ")
    url = input("URL: ")
    return f"[{label}]({url})"

def listing(format, f_texts):
    info = []
    if f_texts:
        info.append("\n")

    while True:
        rows = int(input("Number of rows: "))

        if rows > 0:
            for row in range(1, rows + 1):
                text = input(f"Row #{row}: ")
                if format == "ordered-list": 
                    info.append(f"{row}. {text}\n")
                else:
                    info.append(f"* {text}\n")
            
            return info
            
        else:
            print("The number of rows should be greater than zero")
            pass

            

f_texts = []
counter = 0

while True:
    if counter == 1:
        format = input("\nChoose a formatter: ")
    else:
        format = input("Choose a formatter: ")

    if format == "!help":
        print("""Available formatters: plain bold italic header link inline-code ordered-list unordered-list new-line
Special commands: !help !done""")
        continue
    
    if format == "!done":
        with open("./markdown_editor/output.md", "w") as stream:
            for text in f_texts:
                stream.write(text)
        break
        
    if format in FORMATTERS:
        if format == "header":
            f_texts.append(header())
        elif format == "plain":
            f_texts.append(plain())
        elif format == "bold": 
            f_texts.append(bold())
        elif format == "italic":
            f_texts.append(italic())
        elif format == "inline-code":
            f_texts.append(inline())
        elif format == "link":
            f_texts.append(link())
        elif format == "ordered-list" or format == "unordered-list":
            for info in listing(format, f_texts):
                f_texts.append(info)

        else:
            f_texts.append("\n")

    else:
        print("Unknown formatting type or command")
        pass
    
    counter = 1
    
    for text in f_texts:
        print(text, end="")
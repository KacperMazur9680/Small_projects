import requests
import lxml.html 
import sys

def items_path(xpath, url):
    try:
        str_html = lxml.html.fromstring(store_content(url))
        items = str_html.xpath(xpath)
        return items
    except:
        sys.exit("Invalid xpath.")

def store_content(url):
    resp = requests.get(url)
    if resp.ok:
        content = resp.text
        return content
    else:
        sys.exit("Invalid url.")

def format_items(items):
    items = [item.text_content() for item in items]
    return [item.strip().replace("\n", " ") for item in items]

def print_list(f_items):
    print()
    print("----------------------------------------------------------------")
    for item in f_items:
        print(item)

def main():
    url = input("Enter you link: ")
    xpath = input("Enter the xpath: ")
    items = items_path(xpath, url)
    f_items = format_items(items)
    print_list(f_items)

if __name__ == "__main__":
    main()


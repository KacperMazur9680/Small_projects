import requests
from bs4 import BeautifulSoup
import string
import os
import sys
import shutil


def article_website(link):
    """Returns a parsed html element"""

    article = link.find_previous("a") 

    article_link = "https://www.nature.com" + article.get("href")
    source = requests.get(article_link)

    if source.status_code == 200:
        return BeautifulSoup(source.content, "html.parser")
    else:
        print(f"The URL returned {source.status_code}!")
        sys.exit(1)


def title_format(raw_title):
    """Returns a formatted name of the article's title, without whitespaces and punctuations"""

    title = raw_title.text
    for char in title:
        if char in string.punctuation:
            title = title.replace(char, "")
            
        if char in string.whitespace:
            title = title.replace(char, "_")

    return title


def articles_content(article):
    """Returns the content of each article"""

    new_soup = article_website(article)

    raw_title = new_soup.find("h1")
    content_raw = new_soup.find("div", {"class":"c-article-body u-clearfix"})

    content = content_raw.text
    title = title_format(raw_title)

    return title, content


def checking_for_old_artcls(num_pages):
    """Deletes old articles before the new one are found"""

    for num in range(1, num_pages+1):
        path = os.path.abspath("Small_projects/web_scraper/")
        for file in os.listdir(path):
            if file.startswith("Page_"):
                shutil.rmtree(f"{path}/{file}")


def save_articles(num, title, content):
    """Saves the articles of each page in a directory named Page_x"""

    dir_path = os.path.abspath(f"Small_projects/web_scraper/Page_{num}")

    try:
        os.mkdir(dir_path)

        with open(f"{dir_path}/" + title + ".txt", "wb") as stream:
            stream.write(content.encode('UTF-8'))

    except FileExistsError:
        with open(f"{dir_path}/" + title + ".txt", "ab") as stream:
            stream.write(content.encode('UTF-8'))


def find_articles(num_pages, article_type):
    """Returns a list of found articles"""

    checking_for_old_artcls(num_pages)

    for num in range(1, num_pages+1):
        url = f"https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={num}"
        r = requests.get(url)

        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            articles = soup.find_all("span", string=article_type) 
            for article in articles:
                title, content = articles_content(article)
                save_articles(num, title, content)

        else:
            print(f"The URL returned {r.status_code}!")
            sys.exit(1)

    print("Done! Check the web_scraper directory for your results!")

    
def main():
    pages = int(input("How many pages to search: "))
    article_type = input("What type of article are you looking for: ")

    find_articles(pages, article_type)


if __name__ == "__main__":
    main()
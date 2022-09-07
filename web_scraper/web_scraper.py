import requests
from bs4 import BeautifulSoup
import string



def return_content(url):

    r = requests.get(url)

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        news = soup.find_all("span", string="News")
        for new in news:
            article = new.find_previous("a")
            article_link = "https://www.nature.com" + article.get("href")
            s = requests.get(article_link)
            sp = BeautifulSoup(s.content, "html.parser")

            title_raw = sp.find("h1")
            content_raw = sp.find(id = "content")

            title = title_raw.text
            content = content_raw.text
            
            for char in title:
                if char in string.punctuation or char == "’" :
                    title = title.replace(char, "")
           
                if char in string.whitespace:
                    title = title.replace(char, "_")

            with open("web_scraper/news/" + title + ".txt", "wb") as stream:
                stream.write(content.encode('UTF-8'))

    else:
        print(f"The URL returned {r.status_code}!")


def main():
    url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3"
    return_content(url)


if __name__ == "__main__":
    main()


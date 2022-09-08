import requests
from bs4 import BeautifulSoup
import string
import os



def return_content(num_pages, article_type):
    for num in range(1, num_pages+1):

        url = f"https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={num}"

        r = requests.get(url)

        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            articles = soup.find_all("span", string=article_type)
            for new in articles:
                article = new.find_previous("a") 
                article_link = "https://www.nature.com" + article.get("href")
                s = requests.get(article_link)
                sp = BeautifulSoup(s.content, "html.parser")

                title_raw = sp.find("h1")
                content_raw = sp.find("div", {"class":"c-article-body u-clearfix"})

                title = title_raw.text
                content = content_raw.text
                
                for char in title:
                    if char in string.punctuation:
                        title = title.replace(char, "")
            
                    if char in string.whitespace:
                        title = title.replace(char, "_")

                try:
                    os.mkdir(f"web_scraper/Page_{num}")

                    with open(f"web_scraper/Page_{num}/" + title + ".txt", "wb") as stream:
                        stream.write(content.encode('UTF-8'))
                except FileExistsError:
                    with open(f"web_scraper/Page_{num}/" + title + ".txt", "ab") as stream:
                        stream.write(content.encode('UTF-8'))

        else:
            print(f"The URL returned {r.status_code}!")
    
    print("Done!")

def main():
    pages = int(input("How many pages to search: "))
    article_type = input("What type of article are you looking for: ")
    return_content(pages, article_type)


if __name__ == "__main__":
    main()


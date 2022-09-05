import requests
from bs4 import BeautifulSoup
import sys


def link_check(url):
    if "https://www.imdb.com/title/" in url:
        check = True
    else:
        check = False
    return check


def description(soup):
    try:
        descrp = soup.find('span', {'data-testid': 'plot-l'})
    except KeyError:
        print("Invalid movie page!")
        sys.exit(2)
    else:
        return descrp.text


def movie_title(soup):
    try:
        title = soup.find('h1')
    except KeyError:
        print("Invalid movie page!")
        sys.exit(2)
    else:
        return title.text


def return_content(url):
    if link_check(url):
        r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    else:
        print("Invalid movie page!")
        sys.exit(1)

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        m_title = movie_title(soup)
        descr = description(soup)
        ingdr = {"title": m_title, "description": descr}
        print(ingdr)
    else:
        print("Invalid quote resource!")


def main():
    url = input("Input the URL:\n")
    return_content(url)


if __name__ == "__main__":
    main()

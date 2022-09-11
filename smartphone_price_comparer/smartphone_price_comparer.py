import sys
from bs4 import BeautifulSoup
import requests
import re

ALLOW_ACCESS = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"


def show_results(phone_names, model, shop):
    phones = {}

    try:
        for info in phone_names:
            pricing = info.find_next("div", {"class": "pricing"})
            price_raw = pricing.find("span", {"class": "whole"})
            price_raw_clean = price_raw.text
            price_clean = price_raw_clean.replace("\n", "").strip()
                    
            phones.update({info.text: price_clean})
                
        for key, value in phones.items():
            print(f"{key} => {value}")

    except AttributeError:
        print(f"{model} not found in {shop}")

def media_markt(brand, model, memory):
    if memory > 128:
        memo = "128-01-gb-i-wiecej"
    elif 64 < memory <= 128:
        memo = "64-01-gb-128-gb"
    elif 32 < memory <= 64:
        memo = "32-01-gb-64-gb"
    elif 16 < memory < 32:
        memo = "16-01-gb-32-gb"
    else:
        memo = ""
    return f"https://mediamarkt.pl/telefony-i-smartfony/smartfony/wszystkie-smartfony.{brand}/&pamiec-wbudowana={memo}&model={model}"

def media_expert(brand, model, page):
    return f"https://www.mediaexpert.pl/smartfony-i-zegarki/smartfony/{brand}/popularne-serie_{model}?page={page}"

def neonet(brand, page):
    return f"https://www.neonet.pl/smartfony-i-navi/smartfony/f/{brand}.html?p={page}"

def euro(model, page):
    return f"https://www.euro.com.pl/telefony-komorkowe,seria!{model},strona-{page}.bhtml"


def search_markt(brand, model, memory):
        shop = "Media Markt"
        model_f = model.replace(" ", "-").lower()
        print(media_markt(brand, model_f, memory))
        markt = requests.get(media_markt(brand, model_f, memory), headers={"User-Agent": ALLOW_ACCESS})

        if markt.status_code == 200:
            soup = BeautifulSoup(markt.content, "html.parser")
            phone_names = soup.find_all("h2", {"class": "title"})

            show_results(phone_names, model, memory)
        
        else:
            print(f"Nope, status code = {markt.status_code}")
            sys.exit(1)
        

def search_expert(brand, model):
    for page in range(4):
        expert = requests.get(media_expert(brand, model, page))


def search_neonet(brand, model):
    for page in range(4):
        neonet_ = requests.get(neonet(brand, page))


def search_euro(brand, model):
    for page in range(4):
        euro_ = requests.get(euro(model, page))
    

def main():
    brand = "apple"  #input("Enter the brand of the smartphone: ")
    model = "iphone 14"  #input("Enter the model of the smartphone: ")
    memory = 128  #input("Enter the memory you are interested in [GB]: ")

    search_markt(brand, model, memory)

if __name__ == "__main__":
    main()
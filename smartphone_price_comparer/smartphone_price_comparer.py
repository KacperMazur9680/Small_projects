import sys
from bs4 import BeautifulSoup
import requests
import re

ALLOW_ACCESS = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"


def show_results_markt(phone_names, model, shop, memory):
    phones = {}

    for info in phone_names:
        pricing = info.find_next("div", {"class": "pricing"})
        price_raw = pricing.find("span", {"class": "whole"})

        try:
            price_raw_clean = price_raw.text
        except AttributeError:
            continue 
        else:
            price_clean = price_raw_clean.replace("\n", "").strip()
                    
        phones.update({info.text: price_clean})
                
    for key, value in phones.items():
        if str(memory) in key:
            print(f"{key} => {value}")

    if len(phones) <= 0:
        print(f"{model} {memory} GB not found in {shop}")

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

def media_expert(brand, model, memory, page):
    model_f = model.replace(" ", "-").lower()
    return f"https://www.mediaexpert.pl/smartfony-i-zegarki/smartfony/pamiec-wbudowana-gb_{memory}/popularne-serie_{brand}-{model_f}?page={page}"

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

            show_results_markt(phone_names, model, shop, memory)
        
        else:
            print(f"ERROR {markt.status_code}")
            sys.exit(1)
        

def search_expert(brand, model, memory):
    shop = "Media Expert"
    model_f = model.replace(" ", "-").lower()
    pages_raw = requests.get(f"https://www.mediaexpert.pl/smartfony-i-zegarki/smartfony/pamiec-wbudowana-gb_{memory}/popularne-serie_{brand}-{model_f}")

    if pages_raw.status_code == 200:
        pages_soup = BeautifulSoup(pages_raw.content, "html.parser")
        pages_html = pages_soup.find("span", {"class": "from"})

        try:
            pages = int(pages_html.text[2:])
        except AttributeError:
            pages = 1

        for page in range(1, pages+1):
            print(media_expert(brand, model, memory, page))
            expert = requests.get(media_expert(brand, model, memory, page), headers={"User-Agent": ALLOW_ACCESS})
            soup = BeautifulSoup(expert.content, "html.parser")

            frst_phone = soup.find("div", {"class": "offers-list"})
            frst_phone_name = frst_phone.find("h2", {"class": "name is-section"}).text.replace("\n", "").strip()

            try:
                frst_phone_price = int(frst_phone.find("div", {"class": "main-price is-big"}).find("span", {"class": "whole"}).text.replace(u"\u202f", ""))
            except AttributeError:
                continue

            phone_names = []
            phone_prices = []

            if frst_phone_name and frst_phone_price:
                phone_names.append(frst_phone_name)
                phone_prices.append(frst_phone_price)

            for object in soup.find_all("span", {"whenvisible": "[object Object]"}):
                phone_name = object.find("h2", {"class": "name is-section"})

                try:
                    phone_price = object.find("div", {"class": "main-price is-big"}).find("span", {"class": "whole"})
                except:
                    continue

                phone_names.append(phone_name.text.replace("\n", "").strip())

                try:
                    phone_price = int(phone_price.text.replace(u"\u202f", ""))
                except AttributeError:
                    continue
                else:
                    phone_prices.append(phone_price)
                
            phones = dict(zip(phone_names, phone_prices))
            model_list = []   
            for key in phones.keys():
                key_ = key.lower()
                name_ = re.search(f"{model}(.*){memory}", key_)
                model_ = name_.group(1)
                if "iphone" in key_:
                    if model_.strip() == "":
                        model_list.append(f"Press ENTER for regular {model}")
                    else:
                        model_list.append(model_.strip())
                else:
                    model_list.append(model_.strip() + str(memory) + "GB")

            model_list = set(model_list)

            models = ", ".join(model_list)

            model_spec = input(f"Which model would you like: [{models}]: ")

            for key, value in phones.items():
                if model_spec == re.search(f"{model}(.*){memory}", key.lower()).group(1).strip(): 
                    print(f"{key} => {value}")
                
            if len(phones) <= 0:
                print(f"{model} {memory} GB not found in {shop}")   

    else:
        print(f"ERROR {pages_raw.status_code}")

def search_neonet(brand, model):
    for page in range(4):
        neonet_ = requests.get(neonet(brand, page))


def search_euro(brand, model):
    for page in range(4):
        euro_ = requests.get(euro(model, page))
    

def main():
    brand = "apple"  #input("Enter the brand of the smartphone: ")
    model = "iphone 12"  #input("Enter the model of the smartphone: ")
    memory = 128  #input("Enter the memory you are interested in [GB]: ")

    # search_markt(brand, model, memory)
    search_expert(brand, model, memory)

if __name__ == "__main__":
    main()
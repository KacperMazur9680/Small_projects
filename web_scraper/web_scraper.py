import requests


def return_content(url):
    r = requests.get(url)
    if r.status_code == 200:
        raw_content = r.json()
        try:
            raw_content["content"]
            
        except KeyError:
            content = "Invalid quote resource!"
        else:
            content = raw_content["content"]

    else:
        content = "Invalid quote resource!"

    return content


def main():
    url = input("Input the URL:\n")
    print(return_content(url))


if __name__ == "__main__":
    main()
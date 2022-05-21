import click
import requests
import lxml.html 

# @click.command()
# @click.argument("url")
# @click.argument("xpath")

url = "https://www.leroymerlin.pl/ogrzewanie/kominy-i-odprowadzanie-spalin,a2031.html"
resp = requests.get(url)

with open("Small_projects/website_item_lister/test.html", "wb") as html:
    html.write(resp.content)

with open("Small_projects/website_item_lister/test.html", encoding="utf-8") as stream:
    content = stream.read()

str_html = lxml.html.fromstring(content)
items = str_html.xpath('//*[@id="product-listing"]/div/a/h3')

for item in items:
    print(item.text_content())

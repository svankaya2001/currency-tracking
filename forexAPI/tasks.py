from time import sleep
from celery import shared_task
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

from .models import Currency

@shared_task

def create_currency():
    print('Collecting crypto data ...')
    req = Request('https://coinmarketcap.com/')
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')

    currencies = bs.find("tbody").find_all("tr")[0:10]
    for i in currencies:
        name = i.find("td", class_ = "cmc-table__cell cmc-table__cell--sticky cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__name").div.a.text
        price = i.find("td", class_ = "cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price").a.text
        change_p = i.find("td", class_ = "cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-24-h").div.text
        M_cap = i.find("td", class_ = "cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__market-cap").div.text
        supply = i.find("td", class_ = "cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__circulating-supply").div.text
        volume = i.find("td", class_ = "cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__volume-24-h").a.text
        print({'name':name, 'price':price, 'change_p':change_p, 'M_cap':M_cap, 'supply':supply, 'volume':volume})

        Currency.objects.create(
            name = name,
            price = price,
            change_p = change_p,
            M_cap= M_cap,
            supply = supply,
            volume = volume,
        )

        sleep(5)

@shared_task
# some heavy stuff here
def update_currency():
    print('Updating crypto data ...')
    req = Request('https://coinmarketcap.com/')
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')

    currencies = bs.find("tbody").find_all("tr")[0:10]
    for i in currencies:
        name = i.find("td", class_ = "cmc-table__cell cmc-table__cell--sticky cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__name").div.a.text
        price = i.find("td", class_ = "cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price").a.text
        change_p = i.find("td", class_ = "cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-24-h").div.text
        M_cap = i.find("td", class_ = "cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__market-cap").div.text
        supply = i.find("td", class_ = "cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__circulating-supply").div.text
        volume = i.find("td", class_ = "cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__volume-24-h").a.text
 
        # create dictionary
        data = {'name':name, 'price':price, 'change_p':change_p, 'M_cap':M_cap, 'supply':supply, 'volume':volume}
        # find the object by filtering and update all fields
        Currency.objects.filter(name=name).update(**data)
 
        sleep(5)

create_currency()

while True:
    sleep(15)
    update_currency()


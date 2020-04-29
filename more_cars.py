import asyncio
import aiohttp
import os

from aiohttp import ClientSession, TCPConnector
import aiofiles

import json

from bs4 import BeautifulSoup

BASE_CARS_PATH = 'cars-data/www.cars-data.com/en'


async def get_ld_json(url, session):
    resp = await session.request("GET", url)
    resp.raise_for_status()
    doc = await resp.text()
    parser = "html.parser"
    soup = BeautifulSoup(doc, parser)
    data = json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))
    row = data_to_row(data)
    return row


def data_to_row(data):
    try:
        if data['weightTotal'] == "":
            weight = 0.0
        else:
            weight = float(data.get('weightTotal', "0.0 kg").split(" ")[0])
        if data['fuelConsumption'] == "":
            fuel = 0.0
        else:
            fuel = float(
                data.get('fuelConsumption', '1,1 l/100 km').split(" ")[0]\
                    .replace(',', '.'))
        row = {
            'type': data['bodyType'],
            'weight': weight * 2.2046, # kg to lbs
            'wheelbase': float(data['wheelbase'].split(' ')[0]) * 0.03937, # mm to inches,
            'height': float(data['height'].split(' ')[0]) * 0.03937, # mm to inches
            'Average MPG': _mpg(fuel)
        }
    except ValueError:
        print(f"can't convert {data}")
        row = None
    return row


def _mpg(lpkm):
    if lpkm == 0.0:
        return lpkm
    # convert liters per 100/km to mpg
    liters_per_km = 100 / lpkm
    liters_per_mile = liters_per_km / 1.609344
    return liters_per_mile * 3.785411784 # liters per gallon

"""
Data collected with the following LFH:
$ wget https://www.cars-data.com/en/en-index.xml  --output-document - | \
  egrep -o "https?://[^<]+.*\/en\/.*" | grep -v sitemap | sed -e 's/<[^>]*>//g'| \
  xargs -I @ wget -r @
"""


async def get_links(file):
    with open(file) as fh:
        soup = BeautifulSoup(fh, 'xml')
        links = [link.string for link in soup.find_all('loc')]
        for link in links:
            async with ClientSession(connector=TCPConnector(ssl=False)) as s:
                try:
                    row = await get_ld_json(link, s)
                except Exception:
                    print(f"unable to fetch {link}")
                if row:
                    async with aiofiles.open('DataSet_Massive_Answers.csv', 'a') as f:
                        await f.write(f"{row['weight']},{row['wheelbase']},{row['Average MPG']},{row['height']},{row['type']}\n")

async def collect_links():
    link_files = []
    for file in os.listdir(BASE_CARS_PATH):
        if file.startswith('types'):
            link_files.append(file)
    await asyncio.gather(*(get_links(f"{BASE_CARS_PATH}/{link}") for link in link_files))

if __name__ == '__main__':
    asyncio.run(collect_links())

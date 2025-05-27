import json

import numpy as np
from bs4 import BeautifulSoup
from bs4.element import Tag
from requests import Session

from get_data_regex import *

sess = Session()
with open("headers/arataki.json", "r") as f:
    header = json.load(f)


def search_manuka_doctor():
    # Request the page.
    response = sess.get(
        url="https://www.manukadoctor.co.nz/collections/umf-manuka-honey",
        headers=header,
        timeout=3,
    )
    assert response.status_code == 200, "Fail to get Woolworths products."
    response_html = BeautifulSoup(response.text, 'html.parser')

    # Get item list.
    products_html = response_html.find("section", {"class": "row row--slim"})
    for product_html in products_html.contents:
        if not isinstance(product_html, Tag):
            continue
        price_html = product_html.find("span", {"class": "sale-price"}) or \
            product_html.find("p", {"class": "product-card-price"})
        price = extract_float(price_html.text)
        name = product_html.find("a", {"class": "h4 product-card-title"}).text
        if not ('MGO' in name or 'UMF' in name):
            continue
        umf, mgo = extract_umf_mgo(name)
        yield {
            'brand': 'manuka doctor',
            'retailer': 'manuka doctor',
            'weight': extract_weight(name),
            'UMF': umf,
            'MGO': mgo or np.nan,
            'price': price,
            'marginal_price': price,
        }

# https://www.aratakihoney.co.nz/collections/manuka-honey
import json
import logging

from bs4 import BeautifulSoup
from requests import Session

from get_data_regex import *

sess = Session()
with open("headers/arataki.json", "r") as f:
    header = json.load(f)


def search_arataki():
    # Request the page.
    response = sess.get(
        url="https://www.aratakihoney.co.nz/collections/manuka-honey",
        headers=header, timeout=3,
    )
    assert response.status_code == 200, "Fail to get Woolworths products."
    response_html = BeautifulSoup(response.text, 'html.parser')

    # Get item list.
    products_js = response_html.find(
        'script', {'id': 'web-pixels-manager-setup'}).text
    products_match = re.search(
        r'webPixelsManagerAPI\.publish\("collection_viewed",\s*({.*?})\)',
        products_js, re.DOTALL
    )
    assert products_match, "Fail to parse Egmont products data."
    products_json = products_match.group(1)
    products = json.loads(products_json)

    for product in products.get('collection', {}).get('productVariants', []):
        name = product.get("product", {}).get("untranslatedTitle", '')
        if not ('MGO' in name or 'UMF' in name):
            continue
        name_no_tm = re.sub("™", "", name)
        umf, mgo = extract_umf_mgo(name_no_tm)
        if not product.get('price', {}).get('currencyCode') == 'NZD':
            logging.warning(f"Retailed by 'Egmont', the currency of the price of {name} "
                            f"is not NZD.")
        price = product.get('price', {}).get('amount')
        yield {
            'brand': 'arataki',
            'retailer': 'arataki',
            'weight': extract_weight(name),
            'UMF': umf,
            'MGO': mgo,
            'price': price,
            'marginal_price': price,
        }

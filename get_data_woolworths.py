# https://www.woolworths.co.nz/shop/searchproducts?search=egmont%20manuka
import json

from requests import Session

from get_data_regex import *

sess = Session()
with open("headers/woolworths.json", "r") as f:
    header = json.load(f)


def search_woolworths():
    # Request the page.
    response = sess.get(
        url="https://www.woolworths.co.nz/api/v1/products",
        headers=header,
        params={
            "target": "search",
            "search": "egmont manuka",
            "inStockProductsOnly": "false",
            "size": "48"
        }
    )
    assert response.status_code == 200, "Fail to get Woolworths products."

    # Get item list.
    products = response.json()
    try:
        # cannot use `get` because possibly: products still exist but value is None
        items = products['products']['items']
    except (KeyError, TypeError):
        return
    for item in items:
        umf, mgo = extract_umf_mgo(item.get('variety', ''))
        if item.get('sku') == "489747":
            mgo = 85  # read from the picture
        price = item.get('price', {}).get('salePrice')
        if item.get('productTag') and item['productTag'].get('tagType') == "IsMultiBuy":
            multi_cup_value = item['productTag'].get('multiBuy', {}).get('multiCupValue')
        else:
            multi_cup_value = price
        yield {
            'brand': item.get('brand'),
            'retailer': 'woolworths',
            'weight': extract_weight(item.get('size', {}).get('volumeSize', '')),
            'UMF': umf,
            'MGO': mgo,
            'price': price,
            'value': multi_cup_value,
        }

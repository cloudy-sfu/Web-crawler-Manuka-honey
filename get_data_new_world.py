# https://www.newworld.co.nz/shop/search?q=egmont%20manuka%20honey
import base64
import json
import logging
import os
import secrets
import string
import urllib.parse
from copy import deepcopy
from time import time

from pandas.core.computation.ops import isnumeric
from requests import Session

from get_data_regex import *

sess = Session()
with open("headers/new_world_newrelic.json", "r") as f:
    header_newrelic = json.load(f)
with open("headers/new_world_products.json", "r") as f:
    header_products = json.load(f)
with open("data/new_world_product_payload.json", "r") as f:
    products_payload = json.load(f)
os.makedirs("results", exist_ok=True)
brand_name_renamer = {
    "egmont honey": "egmont"
}

def search_new_world(brand: str, store_id: str):
    searching_query = f"{brand} manuka honey"
    timestamp_ms = int(time() * 1000)

    # Generate newrelic dict.
    new_relic = {
        "v": [0, 1],
        "d": {
            "ty": "Browser",
            "ac": "1811123",
            "ap": "1120226693",
            "id": ''.join(secrets.choice(string.ascii_lowercase + string.digits)
                          for _ in range(16)),
            "tr": ''.join(secrets.choice(string.ascii_lowercase + string.digits)
                          for _ in range(32)),
            "ti": timestamp_ms,
            "tk": "1592950"
        }
    }
    new_relic_str = json.dumps(new_relic, separators=(',', ':'))
    new_relic_base64 = base64.b64encode(new_relic_str.encode('utf-8')).decode('utf-8')

    # Define referer.
    searching_query_quoted = urllib.parse.quote(searching_query)
    referer = f"https://www.newworld.co.nz/shop/search?q={searching_query_quoted}"

    # Get the token and expiry date.
    header_newrelic_ins = deepcopy(header_newrelic)
    header_newrelic_ins['newrelic'] = new_relic_base64
    header_newrelic_ins['referer'] = referer
    current_user_resp = sess.get(
        url="https://www.newworld.co.nz//CommonApi/Account/GetCurrentUser",
        headers=header_newrelic_ins,
    )
    assert current_user_resp.status_code == 200, "Fail to request New World products list."
    token_dict = current_user_resp.json()
    token = token_dict.get('access_token', '')

    # Set payload to request products.
    products_payload_ins = deepcopy(products_payload)
    products_payload_ins['algoliaQuery']['query'] = searching_query
    products_payload_ins['algoliaQuery']['filters'] += store_id
    products_payload_ins['storeId'] = store_id

    # Get product list.
    header_products_ins = deepcopy(header_products)
    header_products_ins['authorization'] += token
    products_resp = sess.post(
        url="https://api-prod.newworld.co.nz/v1/edge/search/paginated/products",
        headers=header_products_ins,
        data=json.dumps(products_payload_ins)
    )
    products_resp_dict = products_resp.json()

    # Validate n_pages = 1
    pages = products_resp_dict.get("totalPages")
    if pages != 1:
        logging.warning("The products list of New World has more than 1 page. This "
                        "program doesn't support multiple pages, please update.")

    products = products_resp_dict.get("products", {})
    for product in products:
        raw_brand = product.get("brand", "").lower()
        umf, mgo = extract_umf_mgo(product.get("name", ""))
        # read the value from the product image.
        if product.get("productId") == "5252782-EA-000":
            mgo = 1046

        # get price
        price = product.get("singlePrice", {}).get("price")
        if not isnumeric(type(price)):
            continue
        price /= 100
        price_value = price
        if isinstance(product.get("promotions"), list):
            for product_promotion in product.get("promotions"):
                proposed_price = product_promotion.get("rewardValue")
                if not isnumeric(type(proposed_price)):
                    continue
                proposed_price /= 100
                if product_promotion.get("multiProducts"):
                    price_value = min(proposed_price, price_value)
                else:
                    price = min(proposed_price, price)
        yield {
            'brand': re.sub("\s*honey\s*", "", raw_brand),
            'retailer': "new_world",
            'weight': extract_weight(product.get("displayName", "")),
            'UMF': umf,
            'MGO': mgo,
            'price': price,
            'value': price_value,
        }

# https://www.egmonthoney.co.nz/collections/umf-manuka-honey
import json
import logging

import demjson3
import pandas as pd
from bs4 import BeautifulSoup
from requests import Session

from get_data_regex import *

sess = Session()
with open("headers/egmont.json", "r") as f:
    header = json.load(f)
egmont_umf_to_mgo = {  # understand from product images
    5: 85, 10: 265, 16: 575,
    20: 830, 23: 1050, 25: 1200
}


def search_egmont():
    # Request the page.
    response = sess.get(
        url="https://www.egmonthoney.co.nz/collections/umf-manuka-honey",
        headers=header, timeout=3,
    )
    assert response.status_code == 200, "Fail to get Egmont independent products."
    response_html = BeautifulSoup(response.text, 'html.parser')

    # Get product list.
    products_js = response_html.find(
        'script', {'id': 'web-pixels-manager-setup'}).text
    products_match = re.search(
        r'\[\\"collection_viewed\\",\s*({.*?})]]\"}\);',
        products_js, re.DOTALL
    )
    assert products_match, "Fail to parse Egmont products data."
    products_json = products_match.group(1)
    products = demjson3.decode(products_json.replace("\\", ""))

    for product in products.get('collection', {}).get('productVariants', []):
        name = product.get("product", {}).get("untranslatedTitle", '')
        if not ('MGO' in name or 'UMF' in name):
            continue
        umf, mgo = extract_umf_mgo(name)
        if not mgo:
            mgo = egmont_umf_to_mgo.get(umf)
        if not product.get('price', {}).get('currencyCode') == 'NZD':
            logging.warning(f"Retailed by 'Egmont', the currency of the price of {name} "
                            f"is not NZD.")
        price = product.get('price', {}).get('amount')
        yield {
            'brand': 'egmont',
            'retailer': 'egmont',
            'weight': extract_weight(name),
            'UMF': umf,
            'MGO': mgo,
            'price': price,
            'marginal_price': price,
        }


def parse_honey_string(title):
    # Separate regex patterns for different components
    num_pattern = re.compile(r"x(\d+)", re.IGNORECASE)
    umf_pattern = re.compile(r"UMF\s+(\d+)\+?", re.IGNORECASE)

    # Extract components individually
    num_match = num_pattern.search(title)
    umf_match = umf_pattern.search(title)

    # Process weight to grams
    weight = extract_weight(title)
    return {
        "num": int(num_match.group(1)),
        "umf": int(umf_match.group(1)),
        "weight": weight
    }


def get_egmont_bundle(single_item: pd.DataFrame):
    bundles = {
        "Soothe & Vitality Bundle":
            "https://www.egmonthoney.co.nz/products/soothe-vitality-manuka-honey-bundle",
        "Intense Support Bundle":
            "https://www.egmonthoney.co.nz/products/intense-support-manuka-honey-bundle"
    }
    for bundle_name, bundle_url in bundles.items():
        response = sess.get(url=bundle_url, headers=header, timeout=3)
        assert response.status_code == 200, "Fail to get Egmont bundle products."
        response_html = BeautifulSoup(response.text, 'html.parser')

        # Get total price.
        try:
            total_price = (response_html.find('sale-price')
                           .find('span', {'class': 'money'}).text)
            total_price = re.search(r"\d+(\.\d{1,2})?", total_price)
            total_price = float(total_price.group())
        except:
            logging.warning(f"Total price of {bundle_name} in Egmont is not parsed.")
            continue
        content = []

        # Get bundle contents.
        raw_bundle_list = response_html.find('ul', {'data-mce-fragment': '1'})
        if not raw_bundle_list:
            logging.warning(f"Products list of {bundle_name} in Egmont is not parsed.")
        for item in raw_bundle_list.find_all('li', {'data-mce-fragment': '1'}):
            content.append(parse_honey_string(item.text))
        content = pd.DataFrame(content)

        # Update "value" column in single items' table.
        content['mgo'] = content['umf'].apply(egmont_umf_to_mgo.get)

        def lookup_price(row):
            # Filter single_item for the same mgo and find the closest weight
            filtered = single_item[single_item["MGO"] == row["mgo"]]
            if not filtered.empty:
                # Find the closest weight
                closest_row = filtered.iloc[
                    (filtered["weight"] - row["weight"]).abs().argsort().iloc[0]
                ]
                # closest_rows.append(closest_row.name)
                return (closest_row["price"] / closest_row["weight"] * row["weight"],
                        int(closest_row.name))

        content[['single_price', 'single_item_idx']] = (
            content.apply(lookup_price, axis=1).apply(pd.Series)
        )
        bundle_discount_ratio = ((content['num'] * content['single_price']).sum()
                                 / total_price)
        content['marginal_price'] = content['single_price'] / max(bundle_discount_ratio, 1)
        single_item.loc[
            content["single_item_idx"], 'marginal_price'
        ] = content['marginal_price'].values

    return single_item

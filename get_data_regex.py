import re

def extract_weight(text):
    """
    :return: Unit: g
    """
    match = re.search(r"(\d+)\s*(g|kg)", text, re.IGNORECASE)
    if match:
        value = int(match.group(1))
        unit = match.group(2).lower()
        if unit == "kg":
            return value * 1000
        return value
    return None

def extract_umf_mgo(title):
    umf_match = re.search(r"(\d+)\s*\+?\s*UMF|UMF\s*\+?\s*(\d+)", title,
                          re.IGNORECASE)
    mgo_match = re.search(r"(\d+)\s*\+?\s*MGO|MGO\s*\+?\s*(\d+)", title,
                          re.IGNORECASE)
    umf = int(umf_match.group(1) or umf_match.group(2)) if umf_match else None
    mgo = int(mgo_match.group(1) or mgo_match.group(2)) if mgo_match else None
    return umf, mgo

def extract_float(s):
    match = re.search(r'\d+\.?\d*', s)
    return float(match.group()) if match else None

if __name__ == '__main__':
    assert extract_umf_mgo("Limited Edition Manuka Honey 23+ UMF") == (23, None)
    assert extract_umf_mgo("Manuka Honey 100+ MGO") == (None, 100)
    assert extract_umf_mgo("umf 5+ monofloral 250g") == (5, None)
    assert extract_umf_mgo("manuka honey umf10 plus mgo 265 pls 250g") == (10, 265)
    assert extract_umf_mgo("egmont manuka honey mgo 100 225g") == (None, 100)

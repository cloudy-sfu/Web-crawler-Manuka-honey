# Web crawler Manuka honey
Compare price of Manuka honey in New Zealand

![](https://shields.io/badge/region-New_Zealand-navy)
![](https://shields.io/badge/dependencies-Python_3.12-blue)

> [!WARNING]
>
> There're evidences that some of these online shopping websites infer users' region via IP address, affecting the currency (therefore incomparable prices). If not in New Zealand, the user may need a proxy.

Included brands:

- EGMONT
- ARATAKI

Included retailers:

- Woolworths
- New World
- Egmont gift shop
- Arataki honey

## Install

Create a Python virtual environment.

Run the following command.

```
pip install -r requirements.txt
```

## Usage

In Python virtual environment, run the following command.

```
python main.py
python visualization.py
```

The result can be found in `results/manuka_honey_price.xlsx`.

In the table, 

- "value": price where T&C applies, like bundles or wholesale discount.

- "UMF" and "MGO": See [UMF organization](https://www.umf.org.nz/unique-manuka-factor/).

>  [!NOTE]
>
> Relationship between UMF and MGO are fitted from data of included brands. Factors excluding MGO have little influence on UMF based on these data.


# Web crawler Manuka honey
Compare price of Manuka honey in New Zealand

![](https://shields.io/badge/region-New_Zealand-navy)
![](https://shields.io/badge/dependencies-Python_3.12-blue)

> [!WARNING]
>
> There're evidences that some of these online shopping websites infer users' region via IP address, affecting the currency (therefore incomparable prices). If not in New Zealand, the user may need a proxy.

Included brands:

- Egmont
- Arataki
- Manuka doctor

Included retailers:

- Woolworths
- New World
- Egmont gift shop
- Arataki honey
- Manuka doctor

## Install

Create a Python 3.12 virtual environment and activate.

Run the following command.

```
pip install -r requirements.txt
```

## Usage

Activate the Python virtual environment.

Run the following command in Windows command prompt (CMD).

```
python main.py
```

The dataset is published at [hugging face](https://huggingface.co/datasets/cloudy-sfu/Manuka-honey).

>  [!NOTE]
>
>  Relationship between UMF and MGO are fitted from data of included brands. Factors excluding MGO have little influence on UMF based on these data.


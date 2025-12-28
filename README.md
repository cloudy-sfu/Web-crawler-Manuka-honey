# Web crawler Manuka honey
Compare price of Manuka honey in New Zealand

![](https://shields.io/badge/region-New_Zealand-navy)
![](https://shields.io/badge/dependencies-Python_3.12-blue)

## Install

Create a Python 3.12 virtual environment and activate.

Run the following command.

```
pip install -r requirements.txt
```

Create a PostgreSQL 17 database in [Neon](https://neon.com/) database, or your own PostgreSQL database.

Run `database_schema.sql` in database console to mock the database schema.

Include the following variables into environment variables.

| Variable | Description                                                  |
| -------- | ------------------------------------------------------------ |
| NEON_DB  | Connection string to Neon database. If using other database, set to connection string of your own PostgreSQL database. |

## Usage

GitHub Actions record current price every Sunday, Thursday 22:00 UTC.

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

>  [!NOTE]
>
>  Relationship between UMF and MGO are fitted from data of included brands. Factors excluding MGO have little influence on UMF based on these data.


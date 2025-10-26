import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text


def mgo_price_weight_fig(price):
    brands = price['brand'].unique()
    fig, ax = plt.subplots(figsize=(12, 8))
    for i in range(len(brands)):
        subset = price[price['brand'] == brands[i]]
        ax.scatter(
            subset['MGO'], subset['marginal_price'],
            s=subset['weight'] * 0.5,
            color=plt.cm.tab10(i % 10),
            alpha=0.5,
            label=brands[i]
        )
    ax.set_xlabel("MGO", fontsize=12)
    ax.set_ylabel("Marginal price (NZD/kg)", fontsize=12)
    ax.grid(True, alpha=0.5)
    ax.set_xlim([0, None])
    ax.set_ylim([0, None])

    brand_handles = [plt.scatter([], [], color=plt.cm.tab10(i))
                      for i in range(len(brands))]
    brand_legend = ax.legend(handles=brand_handles, labels=brands.tolist(),
                             title="Brand", loc='upper left', fontsize=12,
                             bbox_to_anchor=(0.1, 1))
    weight_labels = np.linspace(0.25, 1, 4).tolist()
    weight_handles = [plt.scatter([], [], s=weight * 500, color='black', alpha=0.5)
                      for weight in weight_labels]
    ax.legend(handles=weight_handles, labels=weight_labels,
              title="Pack size (kg)", loc='upper left', fontsize=12,
              labelspacing=1.25, bbox_to_anchor=(0, 1))
    ax.add_artist(brand_legend)

    fig.tight_layout()
    return fig


if __name__ == '__main__':
    engine = create_engine(os.environ['NEON_DB'])
    with engine.begin() as c:
        query_1 = c.execute(text("select max(\"updated_time\") from prices"))
        last_updated_date = query_1.fetchone()[0]
        honey = pd.read_sql_query(
            sql="select * from prices where \"updated_time\" = %(last_updated_date)s",
            con=c,
            params={"last_updated_date": last_updated_date},
        )

    fig = mgo_price_weight_fig(honey)
    fig.text(
        0.01, 0.01,
        f'Updated at {last_updated_date.strftime("%Y-%m-%d %H:%M:%S%z")}',
        ha='left', fontsize=10
    )
    fig.savefig("results/current_prices.pdf")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('results/manuka_honey_price.xlsx')

brands = df['brand'].unique()
fig, ax = plt.subplots(figsize=(12, 8))
for i in range(len(brands)):
    subset = df[df['brand'] == brands[i]]
    ax.scatter(
        subset['MGO'], subset['value'] / subset['weight'] * 1000,
        s=subset['weight'] * 0.5,
        color=plt.cm.tab10(i % 10),
        alpha=0.5,
        label=brands[i]
    )
ax.set_xlabel("MGO", fontsize=12)
ax.set_ylabel("Value (NZD/kg)", fontsize=12)
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
weight_legend = ax.legend(handles=weight_handles, labels=weight_labels,
                          title="Pack size (kg)", loc='upper left', fontsize=12,
                          labelspacing=1.25, bbox_to_anchor=(0, 1))
ax.add_artist(brand_legend)

fig.tight_layout()
fig.savefig("results/manuka_honey_price.pdf")

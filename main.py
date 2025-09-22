import os

import pandas as pd

from get_data_arataki import search_arataki
from get_data_egmont import search_egmont, get_egmont_bundle
from get_data_manuka_doctor import search_manuka_doctor
from get_data_new_world import search_new_world
from get_data_woolworths import search_woolworths
from umf_mgo_conversion import mgo_to_umf, umf_to_mgo
from visualization import mgo_price_weight_fig

# %% Get data.
honey = []
honey_woolworth = search_woolworths(search_word="egmont manuka")
if honey_woolworth:
    honey.append(pd.DataFrame(honey_woolworth))
honey_new_world_egmont = search_new_world(
    brand="egmont",
    # city center metro, has most honey's searching results by experience
    store_id="38b074c4-0e5a-4bd5-b743-d30f28d94982",
)
if honey_new_world_egmont:
    honey.append(pd.DataFrame(honey_new_world_egmont))
honey_new_world_arataki = search_new_world(
    brand="arataki",
    store_id="38b074c4-0e5a-4bd5-b743-d30f28d94982",
)
if honey_new_world_arataki:
    honey.append(pd.DataFrame(honey_new_world_arataki))
honey_egmont = search_egmont()
if honey_egmont:
    honey_egmont = pd.DataFrame(honey_egmont)
    honey.append(honey_egmont)
    honey.append(get_egmont_bundle(honey_egmont))
honey_arataki = search_arataki()
if honey_arataki:
    honey.append(pd.DataFrame(honey_arataki))
honey_doctors = search_manuka_doctor()
if honey_doctors:
    honey.append(pd.DataFrame(honey_doctors))
honey_woolworth_doctors = search_woolworths(search_word="manuka \"doctor\"")
if honey_woolworth_doctors:
    honey.append(pd.DataFrame(honey_woolworth_doctors))

# %% Pre-processing.
honey = pd.concat(honey, axis=0, ignore_index=True)
honey.dropna(subset=['UMF', 'MGO'], how='all', inplace=True)
# pandas.DataFrame.fillna doesn't accept a function.
honey['UMF'] = honey.apply(lambda row: mgo_to_umf(row['MGO'])
if pd.isna(row['UMF']) and not pd.isna(row['MGO']) else row['UMF'], axis=1)
honey['MGO'] = honey.apply(lambda row: umf_to_mgo(row['UMF'])
if pd.isna(row['MGO']) and not pd.isna(row['UMF']) else row['MGO'], axis=1)
now = pd.Timestamp('now', tz='Pacific/Auckland')
honey.insert(loc=0, column="date", value=now.strftime("%Y-%m-%d"))

# %% Export.
output_path = f"results/{now.strftime("%Y-%m")}/{now.strftime("%Y-%m-%d")}"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

honey.to_csv(output_path + ".csv", index=False)
fig = mgo_price_weight_fig(honey)
fig.text(0.01, 0.01, f'Updated at {now.strftime("%Y-%m-%d %H:%M:%S %z")}',
         ha='left', fontsize=10)
fig.savefig("results/Current price report.pdf")

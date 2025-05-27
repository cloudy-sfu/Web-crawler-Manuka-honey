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
honey_woolworth = pd.DataFrame(iter(search_woolworths(
    search_word="egmont manuka",
)))
honey_new_world_egmont = pd.DataFrame(iter(search_new_world(
    brand="egmont",
    # city center metro, has most honey's searching results by experience
    store_id="38b074c4-0e5a-4bd5-b743-d30f28d94982",
)))
honey_new_world_arataki = pd.DataFrame(iter(search_new_world(
    brand="arataki",
    store_id="38b074c4-0e5a-4bd5-b743-d30f28d94982",
)))
honey_egmont = pd.DataFrame(iter(search_egmont()))
honey_egmont = get_egmont_bundle(honey_egmont)
honey_arataki = pd.DataFrame(iter(search_arataki()))
honey_doctors = pd.DataFrame(iter(search_manuka_doctor()))
honey_woolworth_doctors = pd.DataFrame(iter(search_woolworths(
    search_word="manuka \"doctor\""
)))

# %% Pre-processing.
honey = pd.concat([honey_woolworth, honey_new_world_arataki, honey_new_world_egmont,
                   honey_egmont, honey_arataki, honey_doctors, honey_woolworth_doctors],
                  axis=0, ignore_index=True)
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

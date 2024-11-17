from get_data_woolworths import search_woolworths
from get_data_new_world import search_new_world
from get_data_egmont import search_egmont, get_egmont_bundle

honey_list = []
for item in search_woolworths():
    honey_list.append(item)

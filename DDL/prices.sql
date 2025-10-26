create table public.prices
(
    updated_time   timestamp with time zone default now(),
    brand          varchar(16),
    retailer       varchar(16),
    weight         smallint,
    "UMF"          smallint,
    "MGO"          smallint,
    price          numeric(6, 2),
    marginal_price numeric(6, 2)
);

comment on table public.prices is 'Manuka honey prices in New Zealand.';

comment on column public.prices.updated_time is 'When the price is observed.';

comment on column public.prices.brand is 'The company who produce the pack.';

comment on column public.prices.retailer is 'The store where the pack is selling.';

comment on column public.prices.weight is 'Weight of the pack. Unit: g';

comment on column public.prices."UMF" is 'Refer to https://www.umf.org.nz/unique-manuka-factor/';

comment on column public.prices."MGO" is 'Refer to https://www.umf.org.nz/unique-manuka-factor/';

comment on column public.prices.price is 'Price per pack. Customers can get at least the corresponding product in this price without extra cost. Unit: NZD';

comment on column public.prices.marginal_price is 'Price per KG. Terms and conditions applied. The cost allocated to the corresponding product in bulk purchase. For example, if the store promotes 500g pack bundles, "1 item $3, any 2 for $5", the price is $3 and the marginal price is $2.5/500g = 5 NZD/kg.';

alter table public.prices
    owner to neondb_owner;


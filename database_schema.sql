--
-- PostgreSQL database dump
--

\restrict y9AQ0wLWJf2SZjH6bCXuaEnDlfQlJp9TdpBKu8oiw7f8MFf5dyMoaKtTWCOKaqX

-- Dumped from database version 17.7 (bdc8956)
-- Dumped by pg_dump version 17.7

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_table_access_method = heap;

--
-- Name: prices; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.prices (
    updated_time timestamp with time zone DEFAULT now(),
    brand character varying(16),
    retailer character varying(16),
    weight smallint,
    "UMF" smallint,
    "MGO" smallint,
    price numeric(6,2),
    marginal_price numeric(6,2)
);


--
-- Name: TABLE prices; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.prices IS 'Manuka honey prices in New Zealand.';


--
-- Name: COLUMN prices.updated_time; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prices.updated_time IS 'When the price is observed.';


--
-- Name: COLUMN prices.brand; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prices.brand IS 'The company who produce the pack.';


--
-- Name: COLUMN prices.retailer; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prices.retailer IS 'The store where the pack is selling.';


--
-- Name: COLUMN prices.weight; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prices.weight IS 'Weight of the pack. Unit: g';


--
-- Name: COLUMN prices."UMF"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prices."UMF" IS 'Refer to https://www.umf.org.nz/unique-manuka-factor/';


--
-- Name: COLUMN prices."MGO"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prices."MGO" IS 'Refer to https://www.umf.org.nz/unique-manuka-factor/';


--
-- Name: COLUMN prices.price; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prices.price IS 'Price per pack. Customers can get at least the corresponding product in this price without extra cost. Unit: NZD';


--
-- Name: COLUMN prices.marginal_price; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.prices.marginal_price IS 'Price per KG. Terms and conditions applied. The cost allocated to the corresponding product in bulk purchase. For example, if the store promotes 500g pack bundles, "1 item $3, any 2 for $5", the price is $3 and the marginal price is $2.5/500g = 5 NZD/kg.';


--
-- PostgreSQL database dump complete
--

\unrestrict y9AQ0wLWJf2SZjH6bCXuaEnDlfQlJp9TdpBKu8oiw7f8MFf5dyMoaKtTWCOKaqX


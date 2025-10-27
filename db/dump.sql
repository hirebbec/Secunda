--
-- PostgreSQL database dump
--
-- Dumped from database version 16.4 (Debian 16.4-1.pgdg120+2)
-- Dumped by pg_dump version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: secunda-db
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO "secunda-db";

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: secunda-db
--

COMMENT ON SCHEMA public IS '';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: activities; Type: TABLE; Schema: public; Owner: secunda-db
--

CREATE TABLE public.activities (
    name character varying NOT NULL,
    parent_id integer,
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone
);


ALTER TABLE public.activities OWNER TO "secunda-db";

--
-- Name: activities_id_seq; Type: SEQUENCE; Schema: public; Owner: secunda-db
--

CREATE SEQUENCE public.activities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.activities_id_seq OWNER TO "secunda-db";

--
-- Name: activities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: secunda-db
--

ALTER SEQUENCE public.activities_id_seq OWNED BY public.activities.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: secunda-db
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO "secunda-db";

--
-- Name: buildings; Type: TABLE; Schema: public; Owner: secunda-db
--

CREATE TABLE public.buildings (
    address character varying NOT NULL,
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL
);


ALTER TABLE public.buildings OWNER TO "secunda-db";

--
-- Name: buildings_id_seq; Type: SEQUENCE; Schema: public; Owner: secunda-db
--

CREATE SEQUENCE public.buildings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.buildings_id_seq OWNER TO "secunda-db";

--
-- Name: buildings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: secunda-db
--

ALTER SEQUENCE public.buildings_id_seq OWNED BY public.buildings.id;


--
-- Name: organizations; Type: TABLE; Schema: public; Owner: secunda-db
--

CREATE TABLE public.organizations (
    name character varying NOT NULL,
    phone_number character varying[] NOT NULL,
    building_id integer NOT NULL,
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone
);


ALTER TABLE public.organizations OWNER TO "secunda-db";

--
-- Name: organizations_id_seq; Type: SEQUENCE; Schema: public; Owner: secunda-db
--

CREATE SEQUENCE public.organizations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.organizations_id_seq OWNER TO "secunda-db";

--
-- Name: organizations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: secunda-db
--

ALTER SEQUENCE public.organizations_id_seq OWNED BY public.organizations.id;


--
-- Name: organizations_to_activities_relationship; Type: TABLE; Schema: public; Owner: secunda-db
--

CREATE TABLE public.organizations_to_activities_relationship (
    organization_id integer NOT NULL,
    activity_id integer NOT NULL,
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.organizations_to_activities_relationship OWNER TO "secunda-db";

--
-- Name: organizations_to_activities_relationship_id_seq; Type: SEQUENCE; Schema: public; Owner: secunda-db
--

CREATE SEQUENCE public.organizations_to_activities_relationship_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.organizations_to_activities_relationship_id_seq OWNER TO "secunda-db";

--
-- Name: organizations_to_activities_relationship_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: secunda-db
--

ALTER SEQUENCE public.organizations_to_activities_relationship_id_seq OWNED BY public.organizations_to_activities_relationship.id;


--
-- Name: activities id; Type: DEFAULT; Schema: public; Owner: secunda-db
--

ALTER TABLE ONLY public.activities ALTER COLUMN id SET DEFAULT nextval('public.activities_id_seq'::regclass);


--
-- Name: buildings id; Type: DEFAULT; Schema: public; Owner: secunda-db
--

ALTER TABLE ONLY public.buildings ALTER COLUMN id SET DEFAULT nextval('public.buildings_id_seq'::regclass);


--
-- Name: organizations id; Type: DEFAULT; Schema: public; Owner: secunda-db
--

ALTER TABLE ONLY public.organizations ALTER COLUMN id SET DEFAULT nextval('public.organizations_id_seq'::regclass);


--
-- Name: organizations_to_activities_relationship id; Type: DEFAULT; Schema: public; Owner: secunda-db
--

ALTER TABLE ONLY public.organizations_to_activities_relationship ALTER COLUMN id SET DEFAULT nextval('public.organizations_to_activities_relationship_id_seq'::regclass);


--
-- Data for Name: activities; Type: TABLE DATA; Schema: public; Owner: secunda-db
--

COPY public.activities (name, parent_id, id, created_at, updated_at) FROM stdin;
Еда	\N	1	2025-10-27 11:36:04.714562+00	\N
Мясная продукция	1	2	2025-10-27 11:36:22.115475+00	\N
Молочная продукция	1	3	2025-10-27 11:36:33.556748+00	\N
Автомобили	\N	4	2025-10-27 11:37:00.412991+00	\N
Грузовые	4	5	2025-10-27 11:40:05.524083+00	\N
Легковые	4	6	2025-10-27 11:40:19.382902+00	\N
Запчасти	6	7	2025-10-27 11:40:31.190337+00	\N
Аксессуары	6	8	2025-10-27 11:40:38.082101+00	\N
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: secunda-db
--

COPY public.alembic_version (version_num) FROM stdin;
3acb81d82275
\.


--
-- Data for Name: buildings; Type: TABLE DATA; Schema: public; Owner: secunda-db
--

COPY public.buildings (address, id, created_at, updated_at, latitude, longitude) FROM stdin;
г. Москва, ул. Ленина 1, офис 3	1	2025-10-27 11:54:32.111763+00	2025-10-27 11:55:00.861825+00	55.978468	37.173329
\.


--
-- Data for Name: organizations; Type: TABLE DATA; Schema: public; Owner: secunda-db
--

COPY public.organizations (name, phone_number, building_id, id, created_at, updated_at) FROM stdin;
ООО “Рога и Копыта”	{2-222-222,3-333-333,8-923-666-13-13}	1	1	2025-10-27 12:12:34.494668+00	\N
ООО Компания	{2-222-222,3-333-333,8-923-666-13-13}	1	2	2025-10-27 12:13:28.714766+00	\N
\.


--
-- Data for Name: organizations_to_activities_relationship; Type: TABLE DATA; Schema: public; Owner: secunda-db
--

COPY public.organizations_to_activities_relationship (organization_id, activity_id, id, created_at, updated_at) FROM stdin;
2	4	4	2025-10-27 12:12:34.494668+00	\N
1	3	2	2025-10-27 12:12:34.494668+00	\N
2	2	3	2025-10-27 12:12:34.494668+00	\N
1	2	1	2025-10-27 12:12:34.494668+00	\N
\.


--
-- Name: activities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: secunda-db
--

SELECT pg_catalog.setval('public.activities_id_seq', 12, true);


--
-- Name: buildings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: secunda-db
--

SELECT pg_catalog.setval('public.buildings_id_seq', 2, true);


--
-- Name: organizations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: secunda-db
--

SELECT pg_catalog.setval('public.organizations_id_seq', 2, true);


--
-- Name: organizations_to_activities_relationship_id_seq; Type: SEQUENCE SET; Schema: public; Owner: secunda-db
--

SELECT pg_catalog.setval('public.organizations_to_activities_relationship_id_seq', 4, true);


--
-- Name: activities activities_name_key; Type: CONSTRAINT; Schema: public; Owner: secunda-db
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_name_key UNIQUE (name);


--
-- Name: activities activities_pkey; Type: CONSTRAINT; Schema: public; Owner: secunda-db
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: secunda-db
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: buildings buildings_address_key; Type: CONSTRAINT; Schema: public; Owner: secunda-db
--

ALTER TABLE ONLY public.buildings
    ADD CONSTRAINT buildings_address_key UNIQUE (address);


--
-- Name: buildings buildings_pkey; Type: CONSTRAINT; Schema: public; Owner: secunda-db
--

ALTER TABLE ONLY public.buildings
    ADD CONSTRAINT buildings_pkey PRIMARY KEY (id);


--
-- Name: organizations organizations_name_key; Type: CONSTRAINT; Schema: public; Owner: secunda-db
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_name_key UNIQUE (name);


--
-- Name: organizations organizations_pkey; Type: CONSTRAINT; Schema: public; Owner: secunda-db
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_pkey PRIMARY KEY (id);


--
-- Name: organizations_to_activities_relationship organizations_to_activities_relationship_organization_id_key; Type: CONSTRAINT; Schema: public; Owner: secunda-db
--

ALTER TABLE ONLY public.organizations_to_activities_relationship
    ADD CONSTRAINT organizations_to_activities_relationship_organization_id_key UNIQUE (organization_id, activity_id);


--
-- Name: organizations_to_activities_relationship organizations_to_activities_relationship_pkey; Type: CONSTRAINT; Schema: public; Owner: secunda-db
--

ALTER TABLE ONLY public.organizations_to_activities_relationship
    ADD CONSTRAINT organizations_to_activities_relationship_pkey PRIMARY KEY (id);


--
-- Name: activities_id_idx; Type: INDEX; Schema: public; Owner: secunda-db
--

CREATE INDEX activities_id_idx ON public.activities USING btree (id);


--
-- Name: buildings_id_idx; Type: INDEX; Schema: public; Owner: secunda-db
--

CREATE INDEX buildings_id_idx ON public.buildings USING btree (id);


--
-- Name: organizations_id_idx; Type: INDEX; Schema: public; Owner: secunda-db
--

CREATE INDEX organizations_id_idx ON public.organizations USING btree (id);


--
-- Name: organizations_to_activities_relationship_id_idx; Type: INDEX; Schema: public; Owner: secunda-db
--

CREATE INDEX organizations_to_activities_relationship_id_idx ON public.organizations_to_activities_relationship USING btree (id);


--
-- Name: activities activities_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: secunda-db
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.activities(id);


--
-- Name: organizations organizations_building_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: secunda-db
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_building_id_fkey FOREIGN KEY (building_id) REFERENCES public.buildings(id);


--
-- Name: organizations_to_activities_relationship organizations_to_activities_relationship_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: secunda-db
--

ALTER TABLE ONLY public.organizations_to_activities_relationship
    ADD CONSTRAINT organizations_to_activities_relationship_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES public.activities(id);


--
-- Name: organizations_to_activities_relationship organizations_to_activities_relationship_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: secunda-db
--

ALTER TABLE ONLY public.organizations_to_activities_relationship
    ADD CONSTRAINT organizations_to_activities_relationship_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: secunda-db
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;


--
-- PostgreSQL database dump complete
--

\unrestrict ZcR0grKGpoqJIjiYntGdwNOHebxCecdYUYW76bNZ0aekd3WurMT6WQtiMcVwgZC


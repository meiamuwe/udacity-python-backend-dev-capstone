--
-- PostgreSQL database dump
--

\restrict F7sGoSSjjblXN0uxwHtcaO2cJwuhZ4f4XTfDaaazifaEmAZGhXBjhQgCQQbOHXs

-- Dumped from database version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)
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

DROP DATABASE IF EXISTS movieworld_test;


--
-- Name: movieworld_test; Type: DATABASE; Schema: -; Owner: movieworld_test
--

CREATE USER movieworld_test WITH ENCRYPTED PASSWORD 'movieworld_test';
CREATE DATABASE movieworld_test WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';


ALTER DATABASE movieworld_test OWNER TO movieworld_test;
GRANT ALL PRIVILEGES ON DATABASE movieworld_test TO movieworld_test;

\unrestrict F7sGoSSjjblXN0uxwHtcaO2cJwuhZ4f4XTfDaaazifaEmAZGhXBjhQgCQQbOHXs
\connect movieworld_test
\restrict F7sGoSSjjblXN0uxwHtcaO2cJwuhZ4f4XTfDaaazifaEmAZGhXBjhQgCQQbOHXs

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: actor; Type: TABLE; Schema: public; Owner: movieworld_tester
--

CREATE TABLE public.actor (
    id character varying(36) NOT NULL,
    name character varying(100) NOT NULL,
    birth_date date NOT NULL
);


ALTER TABLE public.actor OWNER TO movieworld_tester;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: movieworld_tester
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO movieworld_tester;

--
-- Name: movie; Type: TABLE; Schema: public; Owner: movieworld_tester
--

CREATE TABLE public.movie (
    id character varying(36) NOT NULL,
    title character varying(255) NOT NULL,
    release_date date NOT NULL
);


ALTER TABLE public.movie OWNER TO movieworld_tester;

--
-- Name: role; Type: TABLE; Schema: public; Owner: movieworld_tester
--

CREATE TABLE public.role (
    id character varying(36) NOT NULL,
    "character" character varying(100) NOT NULL,
    movie_id character varying(36) NOT NULL,
    actor_id character varying(36)
);


ALTER TABLE public.role OWNER TO movieworld_tester;

--
-- Data for Name: actor; Type: TABLE DATA; Schema: public; Owner: movieworld_tester
--

INSERT INTO public.actor VALUES ('4cf6fc17-b62c-41e9-8dc0-429369dc1225', 'Keira Knightley', '1985-03-26');
INSERT INTO public.actor VALUES ('cd604e70-9bef-41ec-8a46-2c4756caf375', 'Diane Keaton', '1946-01-05');
INSERT INTO public.actor VALUES ('624efc05-ebe4-40c8-9975-cbb0c1f0f32a', 'Woody Allen', '1935-11-30');


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: movieworld_tester
--

INSERT INTO public.alembic_version VALUES ('e7f8bea7030c');


--
-- Data for Name: movie; Type: TABLE DATA; Schema: public; Owner: movieworld_tester
--

INSERT INTO public.movie VALUES ('dcc12f27-03eb-4bf9-96d9-c08c27e6daa0', 'Annie Hall', '1977-04-20');
INSERT INTO public.movie VALUES ('9de51b34-ffa4-4ce7-896b-75d508c4e0aa', 'Reds', '1981-12-25');
INSERT INTO public.movie VALUES ('34f64801-5932-4f06-9c50-383b21acc7eb', 'The Shawshank Redemption', '1994-10-14');


--
-- Data for Name: role; Type: TABLE DATA; Schema: public; Owner: movieworld_tester
--

INSERT INTO public.role VALUES ('01c60191-d6f1-4fa5-95c0-0511c0f2e651', 'Alvy Singer', 'dcc12f27-03eb-4bf9-96d9-c08c27e6daa0', '624efc05-ebe4-40c8-9975-cbb0c1f0f32a');
INSERT INTO public.role VALUES ('f36877c1-c73c-4ab2-bb05-42a455a16302', 'Annie Hall', 'dcc12f27-03eb-4bf9-96d9-c08c27e6daa0', 'cd604e70-9bef-41ec-8a46-2c4756caf375');
INSERT INTO public.role VALUES ('24a7ef79-9f52-419c-ab8f-82283afa6ca7', 'Louise Bryant', '9de51b34-ffa4-4ce7-896b-75d508c4e0aa', 'cd604e70-9bef-41ec-8a46-2c4756caf375');
INSERT INTO public.role VALUES ('e5fe8eee-adfd-4b64-a15c-20431ea35e1f', 'John Reed', '9de51b34-ffa4-4ce7-896b-75d508c4e0aa', NULL);
INSERT INTO public.role VALUES ('5bda8967-ebc4-4946-9274-8d850eefb7ba', 'Ellis Boyd ''Red'' Redding', '34f64801-5932-4f06-9c50-383b21acc7eb', NULL);


--
-- Name: role _role_movie_id_character_uc; Type: CONSTRAINT; Schema: public; Owner: movieworld_tester
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT _role_movie_id_character_uc UNIQUE (movie_id, "character");


--
-- Name: actor actor_pkey; Type: CONSTRAINT; Schema: public; Owner: movieworld_tester
--

ALTER TABLE ONLY public.actor
    ADD CONSTRAINT actor_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: movieworld_tester
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: movie movie_pkey; Type: CONSTRAINT; Schema: public; Owner: movieworld_tester
--

ALTER TABLE ONLY public.movie
    ADD CONSTRAINT movie_pkey PRIMARY KEY (id);


--
-- Name: role role_pkey; Type: CONSTRAINT; Schema: public; Owner: movieworld_tester
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (id);


--
-- Name: ix_role_movie_id; Type: INDEX; Schema: public; Owner: movieworld_tester
--

CREATE INDEX ix_role_movie_id ON public.role USING btree (movie_id);


--
-- Name: role role_actor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: movieworld_tester
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_actor_id_fkey FOREIGN KEY (actor_id) REFERENCES public.actor(id) ON DELETE RESTRICT;


--
-- Name: role role_movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: movieworld_tester
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movie(id) ON DELETE CASCADE;


--
-- postgresQL database dump complete
--

\unrestrict F7sGoSSjjblXN0uxwHtcaO2cJwuhZ4f4XTfDaaazifaEmAZGhXBjhQgCQQbOHXs


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
DROP USER IF EXISTS movieworld_test;


--
-- Name: movieworld_test; Type: DATABASE; Schema: -; Owner: movieworld_test
--

CREATE USER movieworld_test WITH ENCRYPTED PASSWORD 'movieworld_test';
CREATE DATABASE movieworld_test WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';


ALTER DATABASE movieworld_test OWNER TO movieworld_test;
GRANT ALL PRIVILEGES ON DATABASE movieworld_test TO movieworld_test;

\unrestrict F7sGoSSjjblXN0uxwHtcaO2cJwuhZ4f4XTfDaaazifaEmAZGhXBjhQgCQQbOHXs


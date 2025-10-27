--
-- PostgreSQL database dump
--


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
-- Data for Name: actor; Type: TABLE DATA; Schema: public; Owner: movieworld_tester
--

INSERT INTO public.actor VALUES ('4cf6fc17-b62c-41e9-8dc0-429369dc1225', 'Keira Knightley', '1985-03-26');
INSERT INTO public.actor VALUES ('cd604e70-9bef-41ec-8a46-2c4756caf375', 'Diane Keaton', '1946-01-05');
INSERT INTO public.actor VALUES ('624efc05-ebe4-40c8-9975-cbb0c1f0f32a', 'Woody Allen', '1935-11-30');


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
-- postgresQL database dump complete
--

\unrestrict F7sGoSSjjblXN0uxwHtcaO2cJwuhZ4f4XTfDaaazifaEmAZGhXBjhQgCQQbOHXs


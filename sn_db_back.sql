--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4

-- Started on 2024-09-10 17:59:35

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
-- TOC entry 215 (class 1259 OID 17096)
-- Name: Friends; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Friends" (
    user_id integer NOT NULL,
    friend_id integer NOT NULL,
    status character varying(30) NOT NULL
);


ALTER TABLE public."Friends" OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 17102)
-- Name: Groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Groups" (
    id bigint NOT NULL,
    type character varying(20) NOT NULL,
    photo_id integer,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    name character varying(100)
);


ALTER TABLE public."Groups" OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 17101)
-- Name: Groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Groups_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Groups_id_seq" OWNER TO postgres;

--
-- TOC entry 4859 (class 0 OID 0)
-- Dependencies: 216
-- Name: Groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Groups_id_seq" OWNED BY public."Groups".id;


--
-- TOC entry 218 (class 1259 OID 17109)
-- Name: Messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Messages" (
    user_id integer NOT NULL,
    group_id integer NOT NULL,
    content text,
    created_at time with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public."Messages" OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 17115)
-- Name: Participants; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Participants" (
    user_id integer NOT NULL,
    group_id integer NOT NULL,
    role character varying(20) NOT NULL,
    created_at time with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public."Participants" OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 17122)
-- Name: Photos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Photos" (
    id integer NOT NULL,
    filename text NOT NULL,
    data bytea NOT NULL
);


ALTER TABLE public."Photos" OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 17130)
-- Name: Photos_Posts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Photos_Posts" (
    "Photos_id" integer NOT NULL,
    "Posts_id" integer NOT NULL
);


ALTER TABLE public."Photos_Posts" OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 17121)
-- Name: Photos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Photos_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Photos_id_seq" OWNER TO postgres;

--
-- TOC entry 4860 (class 0 OID 0)
-- Dependencies: 220
-- Name: Photos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Photos_id_seq" OWNED BY public."Photos".id;


--
-- TOC entry 224 (class 1259 OID 17134)
-- Name: Posts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Posts" (
    id bigint NOT NULL,
    author_id integer NOT NULL,
    message text
);


ALTER TABLE public."Posts" OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 17133)
-- Name: Posts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Posts_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Posts_id_seq" OWNER TO postgres;

--
-- TOC entry 4861 (class 0 OID 0)
-- Dependencies: 223
-- Name: Posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Posts_id_seq" OWNED BY public."Posts".id;


--
-- TOC entry 226 (class 1259 OID 17143)
-- Name: Users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Users" (
    id bigint NOT NULL,
    username character varying(100) NOT NULL,
    email character varying(150) NOT NULL,
    password text NOT NULL,
    photo_id integer
);


ALTER TABLE public."Users" OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 17142)
-- Name: Users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Users_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Users_id_seq" OWNER TO postgres;

--
-- TOC entry 4862 (class 0 OID 0)
-- Dependencies: 225
-- Name: Users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Users_id_seq" OWNED BY public."Users".id;


--
-- TOC entry 4665 (class 2604 OID 17105)
-- Name: Groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Groups" ALTER COLUMN id SET DEFAULT nextval('public."Groups_id_seq"'::regclass);


--
-- TOC entry 4669 (class 2604 OID 17125)
-- Name: Photos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Photos" ALTER COLUMN id SET DEFAULT nextval('public."Photos_id_seq"'::regclass);


--
-- TOC entry 4670 (class 2604 OID 17137)
-- Name: Posts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Posts" ALTER COLUMN id SET DEFAULT nextval('public."Posts_id_seq"'::regclass);


--
-- TOC entry 4671 (class 2604 OID 17146)
-- Name: Users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Users" ALTER COLUMN id SET DEFAULT nextval('public."Users_id_seq"'::regclass);


--
-- TOC entry 4842 (class 0 OID 17096)
-- Dependencies: 215
-- Data for Name: Friends; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Friends" (user_id, friend_id, status) FROM stdin;
\.


--
-- TOC entry 4844 (class 0 OID 17102)
-- Dependencies: 217
-- Data for Name: Groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Groups" (id, type, photo_id, created_at, name) FROM stdin;
\.


--
-- TOC entry 4845 (class 0 OID 17109)
-- Dependencies: 218
-- Data for Name: Messages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Messages" (user_id, group_id, content, created_at) FROM stdin;
\.


--
-- TOC entry 4846 (class 0 OID 17115)
-- Dependencies: 219
-- Data for Name: Participants; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Participants" (user_id, group_id, role, created_at) FROM stdin;
\.


--
-- TOC entry 4848 (class 0 OID 17122)
-- Dependencies: 221
-- Data for Name: Photos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Photos" (id, filename, data) FROM stdin;
\.


--
-- TOC entry 4849 (class 0 OID 17130)
-- Dependencies: 222
-- Data for Name: Photos_Posts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Photos_Posts" ("Photos_id", "Posts_id") FROM stdin;
\.


--
-- TOC entry 4851 (class 0 OID 17134)
-- Dependencies: 224
-- Data for Name: Posts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Posts" (id, author_id, message) FROM stdin;
\.


--
-- TOC entry 4853 (class 0 OID 17143)
-- Dependencies: 226
-- Data for Name: Users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Users" (id, username, email, password, photo_id) FROM stdin;
\.


--
-- TOC entry 4863 (class 0 OID 0)
-- Dependencies: 216
-- Name: Groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Groups_id_seq"', 1, false);


--
-- TOC entry 4864 (class 0 OID 0)
-- Dependencies: 220
-- Name: Photos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Photos_id_seq"', 1, false);


--
-- TOC entry 4865 (class 0 OID 0)
-- Dependencies: 223
-- Name: Posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Posts_id_seq"', 1, false);


--
-- TOC entry 4866 (class 0 OID 0)
-- Dependencies: 225
-- Name: Users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Users_id_seq"', 1, false);


--
-- TOC entry 4673 (class 2606 OID 17100)
-- Name: Friends Friends_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Friends"
    ADD CONSTRAINT "Friends_pkey" PRIMARY KEY (user_id, friend_id);


--
-- TOC entry 4675 (class 2606 OID 17108)
-- Name: Groups Groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Groups"
    ADD CONSTRAINT "Groups_pkey" PRIMARY KEY (id);


--
-- TOC entry 4679 (class 2606 OID 17129)
-- Name: Photos Photos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Photos"
    ADD CONSTRAINT "Photos_pkey" PRIMARY KEY (id);


--
-- TOC entry 4681 (class 2606 OID 17141)
-- Name: Posts Posts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Posts"
    ADD CONSTRAINT "Posts_pkey" PRIMARY KEY (id);


--
-- TOC entry 4677 (class 2606 OID 17120)
-- Name: Participants Public_participants_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Participants"
    ADD CONSTRAINT "Public_participants_pkey" PRIMARY KEY (user_id, group_id);


--
-- TOC entry 4683 (class 2606 OID 17150)
-- Name: Users Users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_pkey" PRIMARY KEY (id);


--
-- TOC entry 4685 (class 2606 OID 17152)
-- Name: Users unique_email; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT unique_email UNIQUE (email);


--
-- TOC entry 4687 (class 2606 OID 17154)
-- Name: Users unique_username; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT unique_username UNIQUE (username);


--
-- TOC entry 4695 (class 2606 OID 17190)
-- Name: Photos_Posts Photos_Posts_Photos_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Photos_Posts"
    ADD CONSTRAINT "Photos_Posts_Photos_id_fkey" FOREIGN KEY ("Photos_id") REFERENCES public."Photos"(id) NOT VALID;


--
-- TOC entry 4696 (class 2606 OID 17195)
-- Name: Photos_Posts Photos_Posts_Posts_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Photos_Posts"
    ADD CONSTRAINT "Photos_Posts_Posts_id_fkey" FOREIGN KEY ("Posts_id") REFERENCES public."Posts"(id) NOT VALID;


--
-- TOC entry 4697 (class 2606 OID 17200)
-- Name: Posts author; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Posts"
    ADD CONSTRAINT author FOREIGN KEY (author_id) REFERENCES public."Users"(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 4688 (class 2606 OID 17155)
-- Name: Friends friend; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Friends"
    ADD CONSTRAINT friend FOREIGN KEY (friend_id) REFERENCES public."Users"(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 4691 (class 2606 OID 17170)
-- Name: Messages group; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Messages"
    ADD CONSTRAINT "group" FOREIGN KEY (group_id) REFERENCES public."Groups"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4693 (class 2606 OID 17180)
-- Name: Participants group; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Participants"
    ADD CONSTRAINT "group" FOREIGN KEY (group_id) REFERENCES public."Groups"(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 4690 (class 2606 OID 17165)
-- Name: Groups photo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Groups"
    ADD CONSTRAINT photo FOREIGN KEY (photo_id) REFERENCES public."Photos"(id) ON UPDATE CASCADE ON DELETE SET NULL NOT VALID;


--
-- TOC entry 4698 (class 2606 OID 17205)
-- Name: Users photo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT photo FOREIGN KEY (photo_id) REFERENCES public."Photos"(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 4689 (class 2606 OID 17160)
-- Name: Friends user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Friends"
    ADD CONSTRAINT "user" FOREIGN KEY (user_id) REFERENCES public."Users"(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 4692 (class 2606 OID 17175)
-- Name: Messages user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Messages"
    ADD CONSTRAINT "user" FOREIGN KEY (user_id) REFERENCES public."Users"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4694 (class 2606 OID 17185)
-- Name: Participants user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Participants"
    ADD CONSTRAINT "user" FOREIGN KEY (user_id) REFERENCES public."Users"(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


-- Completed on 2024-09-10 17:59:35

--
-- PostgreSQL database dump complete
--


--
-- PostgreSQL database dump
--

-- Dumped from database version 14.15 (Homebrew)
-- Dumped by pg_dump version 14.15 (Homebrew)

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: jake
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO jake;

--
-- Name: diaries; Type: TABLE; Schema: public; Owner: jake
--

CREATE TABLE public.diaries (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    content text NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.diaries OWNER TO jake;

--
-- Name: diaries_id_seq; Type: SEQUENCE; Schema: public; Owner: jake
--

CREATE SEQUENCE public.diaries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.diaries_id_seq OWNER TO jake;

--
-- Name: diaries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jake
--

ALTER SEQUENCE public.diaries_id_seq OWNED BY public.diaries.id;


--
-- Name: diary_images; Type: TABLE; Schema: public; Owner: jake
--

CREATE TABLE public.diary_images (
    id integer NOT NULL,
    filename character varying(255) NOT NULL,
    diary_id integer NOT NULL,
    created_at timestamp without time zone,
    is_representative boolean DEFAULT false NOT NULL
);


ALTER TABLE public.diary_images OWNER TO jake;

--
-- Name: diary_images_id_seq; Type: SEQUENCE; Schema: public; Owner: jake
--

CREATE SEQUENCE public.diary_images_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.diary_images_id_seq OWNER TO jake;

--
-- Name: diary_images_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jake
--

ALTER SEQUENCE public.diary_images_id_seq OWNED BY public.diary_images.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: jake
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    password_hash character varying(200) NOT NULL,
    created_at timestamp without time zone,
    gpt_api_key_encrypted character varying(500)
);


ALTER TABLE public.users OWNER TO jake;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: jake
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO jake;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jake
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: diaries id; Type: DEFAULT; Schema: public; Owner: jake
--

ALTER TABLE ONLY public.diaries ALTER COLUMN id SET DEFAULT nextval('public.diaries_id_seq'::regclass);


--
-- Name: diary_images id; Type: DEFAULT; Schema: public; Owner: jake
--

ALTER TABLE ONLY public.diary_images ALTER COLUMN id SET DEFAULT nextval('public.diary_images_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: jake
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: jake
--

COPY public.alembic_version (version_num) FROM stdin;
97117f1d0a5b
\.


--
-- Data for Name: diaries; Type: TABLE DATA; Schema: public; Owner: jake
--

COPY public.diaries (id, title, content, created_at, updated_at, user_id) FROM stdin;
6	이미지가 업로드	이미지가 업로드 되는 거 확인하고 싶습니다	2025-02-05 00:00:00	2025-02-07 13:43:24.231164	1
7	내가 사랑하는 것	우리가 사랑하는 것들이 있습니다. 이 모든 것들이 다 아름답고 예쁜 것으로 나타나기를 바라 봅니다. 감사합니다.	2025-02-12 00:00:00	2025-02-07 13:46:33.505611	1
8	다시 또 작성해보자	📌 맥 크롬(Chrome)에서 개발자 도구 콘솔에서 days_in_month 값 확인하는 방법\r\n\r\n🚀 브라우저의 개발자 도구(DevTools)를 사용하면 days_in_month 값이 제대로 전달되는지 확인할 수 있어!\r\n아래 단계에 따라 진행해 보자.\r\n\r\n🔹 1️⃣ 크롬 개발자 도구(DevTools) 열기\r\n\t1.\t크롬에서 개발자 도구를 여는 방법:\r\n\t•\t단축키: ⌘ + ⌥ + I (Command + Option + I)\r\n\t•\t메뉴: 보기(View) > 개발자 > 개발자 도구\r\n\t2.\t개발자 도구(DevTools)에서 “콘솔(Console)” 탭 클릭\r\n\t•\t개발자 도구가 열리면 “Console” 탭을 클릭!\r\n\t•\t또는 단축키 ⌘ + ⌥ + J (Command + Option + J)로 바로 콘솔 실행\r\n\r\n🔹 2️⃣ days_in_month 값 확인하는 방법\r\n\r\n✅ 방법 1: 콘솔에서 직접 입력하여 확인\r\n\r\n콘솔에서 다음 명령어를 입력하고 Enter를 누르면 현재 days_in_month 값이 출력돼.\r\n\r\nconsole.log(days_in_month);\r\n\r\n📌 만약 ReferenceError: days_in_month is not defined 오류가 나오면, 해당 변수가 전역 범위(window)에 정의되지 않았을 가능성이 있어.\r\n\r\n✅ 방법 2: window 객체에서 확인\r\n\r\n변수가 window 객체의 속성이라면, 다음과 같이 window.days_in_month를 입력하여 확인할 수 있어.\r\n\r\nconsole.log(window.days_in_month);\r\n\r\n🚀 출력 결과를 확인하고, 기대한 값이 나오는지 체크해 보자!\r\n\r\n✅ 방법 3: 특정 함수에서 days_in_month 값 확인하기\r\n\r\n만약 days_in_month가 특정 함수 내부에서만 존재하는 값이라면,\r\n해당 함수 안에서 console.log()를 추가하고 실행해 보자.\r\n\r\nfunction getDaysInMonth(month, year) {\r\n    let days_in_month = new Date(year, month, 0).getDate();\r\n    console.log("days_in_month 값:", days_in_month); // 🔥 확인용 로그\r\n    return days_in_month;\r\n}\r\n\r\n🚀 이제 getDaysInMonth(2, 2024);를 실행하면 콘솔에 값이 출력될 거야!\r\n\r\n📌 3️⃣ 네트워크 요청에서 days_in_month 값 확인\r\n\r\n만약 days_in_month 값이 서버에서 전달되는 값이라면,\r\n네트워크 요청을 확인해서 올바르게 전달되고 있는지 확인해야 해.\r\n\r\n✅ 방법\r\n\t1.\t개발자 도구(DevTools)에서 “네트워크(Network)” 탭 열기\r\n\t2.\t페이지에서 days_in_month가 포함된 요청을 실행\r\n\t3.\t요청 목록에서 관련된 API 요청 선택\r\n\t4.\t“Preview” 또는 “Response”에서 days_in_month 값 확인\r\n\r\n📌 최종 정리\r\n\r\n작업\t단축키\r\n개발자 도구(DevTools) 열기\t⌘ + ⌥ + I\r\n콘솔(Console) 바로 열기\t⌘ + ⌥ + J\r\n콘솔에서 변수 값 확인\tconsole.log(days_in_month);\r\n네트워크 요청 값 확인\t“Network” 탭에서 API 응답 확인\r\n\r\n✅ 이제 days_in_month 값이 제대로 전달되는지 확인할 수 있어! 🚀\r\n추가로 궁금한 점 있으면 언제든 질문해 줘! 😊	2025-02-13 00:00:00	2025-02-07 13:48:20.424263	1
9	글을 작성해보자.	<p>&nbsp;</p>\r\n<p>이렇게 해서 작성을 한다는 거군야?</p>\r\n<p>&nbsp;</p>\r\n<p>맞는 거야?</p>\r\n<h1>그런데 마크다운은 다시 작동 안 하는 거야?</h1>\r\n<h3>작동하겠지?</h3>\r\n<p>&nbsp;</p>\r\n<p>엔터를 치면 작동하는구만 뭘..</p>\r\n<p>&nbsp;</p>\r\n<p>&nbsp;</p>\r\n<p>&nbsp;</p>\r\n<p><img src="../static/uploads/15173799-f76f-4d1b-a0bf-8ceb6017b934.jpg" alt="" width="1028" height="771"></p>	2025-02-07 00:00:00	2025-02-07 13:59:40.26054	1
10	제목이 항상 필요해	<p>나름대로 좋은 툴이라고 생각했다.</p>\r\n<p>그런데 그게 아니었을 수도 있겠단 생각이 들었던 거다.</p>\r\n<p>내가 지금 다운 받은 에디터는 어디에서 받은 거고, 어떻게 작동하는지, 알기는 하는 거냐?</p>\r\n<p>&nbsp;</p>	2025-02-07 00:00:00	2025-02-07 14:00:43.004168	1
11	새벽이 힘들었던	<p>### Summary Today</p>\r\n<p><br>### Permanent Note</p>\r\n<p><br>### Day Records<br>- 04:00 - 06:00 새벽에 좀 힘들었다. 어제 잠을 조금 늦게 잔 것도 있고, 주호가 새벽 4시부터 일어나서 나를 깨웠다. 나가고 싶어서 우는데 절대로 나갈 수가 없었다. 그러면 안 될 것 같았다. 그런데 이렇게 끌려가면서 하루를 시작하다 보니 확실히 하루가 컨디션이 안 좋은 것 같다. 내가 더 의도하고 이끌어가는 하루로 만들어야 하는데 시작부터 그러지 못해서 2시간 동안 앉아서 울고 있었을 주호한테도 너무 미안하고, 그 두 시간을 버틴다고 해서 컨디션이 좋아지지도 않은 나한테도 미안하고 그렇다.<br>- 06:00 - 09:00 아침에 주호 밥을 먹이고 장모님께서 설날이라고 음식을 하시는 동안에도 나는 컨디션이 너무 좋지 않았다. 힘들었다. 더 자고 싶은 생각도 들었고 뭔가 에너지도 나지도 않고 힘들었다. 한나는 변비약을 먹어서 화장실을 여러 번 왔다 갔다 했는데 그때마다 내가 한나한테 의지하고 싶은데 한나가 없어서 더 힘들었다. 예민해졌다. 주호를 방으로 데리고 와서 어제 하루를 기록하면서 나를 돌아보게 된다. 그래도 오늘 메멘토몰이를 생각하자. 마지막 날이라고 생각하고 정말 의미 있는 하루를 만들기 위해 오늘도 노력해보자. 열심히 해보자.<br>- 09:00 - 12:00 장모님께서 설날이기 때문에 식사를 준비하셨다. 간단하게 애호박나물도 하시고 육전도 만드시고 잡채도 만드셨다. 겉절이까지 순식간에 만드셨다. 우리는 대웅이를 기다릴까 하다가 점심을 조금 이르게 먹었다. 주호가 자고 있을 때였다. 나는 떡국을 끓였고, 떡국에 만두 그리고 평소에 장모님은 넣지 않으신다고 하는 두부까지 왕창 넣어서 내 스타일대로 떡국을 끓여서 같이 먹었다. 탄수화물을 먹었는데도 불구하고 혈당이 거의 오르지 않았다. 만족할 만한 그런 식사였다. 하지만 뭔가 자꾸만 몸이 처지는 그런 느낌을 받고 있었다.<br>- 12:00 - 14:00 주호가 일어나서 주호 밥을 먹이고 그 사이 가족들은 집을 정리를 했다. 그리고 쉬는 인터벌 훈련을 했다. 그렇게 25세트를 달렸으니 총 5km를 했다. 생각보다 이게 힘들었고 또 재밌었다. 먼저 힘들었던 건 내가 빠른 속도로 달리게 되다 보니 내 체중을 아직은 다리가 감당하기가 힘든 것 같았다. 그래서 앞꿈치로 걸을 때 조금 무리가 오는 것 같은 느낌이 들었다. 처음에는 앞꿈치에 힘이 있기 때문에 그나마 괜찮았지만, 뒤로 가면 갈수록 다리가 흔들릴 것 같은 그런 불안한 느낌도 들었다. 그렇게 힘들었지만 또 한편으로 너무 재밌었던 건 내가 의식적인 훈련을 통해서 능력을 키워 나가고 있다는 그런 느낌이 들었기 때문이다. 작은 달리기에 불과하지만 이 달리기엔 정말 많은 게 담겨 있다. 작년에는 포기하지 않겠다는 그런 일념, 열 번을 완주하겠다는 어떤 목표 이런 것들을 이뤄나가는 그런 성취감들이 작년에는 참 좋았는데, 이번에는 2025년엔 이것들을 더 정교하게 다듬고 더 나은 방향으로 만들기 위해서 노력하는 게 그게 굉장히 기분이 좋다. 그래서 앞으로 200m 달리고 100m를 회복하는 인터벌도 해볼 거고, 이걸 계속해 나가다 보면 어제 100m를 달린 속도가 거의 30초 정도 나왔는데 그 속도로 10km를 완주해야 그래야만 목표하는 기록을 낼 수 있기 때문에 이 훈련을 계속하면서 달릴 수 있는 거리를 늘려 나가는 거, 이게 나한테 정말 필요한 훈련이라는 생각을 하게 됐다. 해보자. 100m 쉬고 회복, 200m 쉬고 회복, 1km 쉬고 회복, 5km 쉬고 회복. 그러다 10km까지 충분히 될 거다. 해낼 수 있다.<br>- 14:00 - 16:00 이때가 정말 힘든 시간이었다. 씻고 나와서 다리가 땡겼고, 주호는 에너지가 정말 넘쳐났고, 나는 오히려 에너지가 떨어지고 있어서 힘들었다. 게다가 놀아줄 것도 마땅치 않았고 몸이 힘드니 아무 생각도 나지는 않았다. 한나도 힘든 얼굴이었고 우리는 모두 지루하게 집에서 머물러 있는 느낌이었다.<br>- 16:00 - 17:30 나가기로 결정했다. 그래서 이마트 트레이더스를 갔다. 코스트코를 갈까 했는데 문을 열지 않았다. 이마트 트레이더스에서 뭘 살지 생각도 없었지만 나간다는 생각, 아이쇼핑만 하자는 생각으로 갔다가 이것저것 사게 됐다. 특히 나에게는 단백질 쉐이크를 산 게 큰 수확이었다. 단백질 쉐이크가 거의 6만 7천 원짜리였는데 너무너무 비싸서 깜짝 놀랐고 영양제도 사고 그렇게 시간을 거의 소진하고 돌아왔다.<br>- 17:30 - 19:00 집에 와서 주호를 씻기고 나와서 주호 밥을 준비를 했다. 주호 밥은 곰국에 밥을 말아서 만들었다. 비율이 굉장히 좋았다고 장모님께서 말씀해주셨다. 그리고 처음으로 주호 수영을 시켰다. 한나가 욕조에 물을 받아놓고 거기서 시켰는데 나는 잠깐 주호가 물놀이를 하는 모습을 봤는데 너무 평온해 보여서 예전에 주호가 물놀이를 하던 때가 생각이 났다. 주호도 앞으로 자주 시켜주면 참 좋을 텐데 하는 그런 생각 들었고. 주호 밥을 먹고 있다가 대웅이가 왔고 내가 가져온 소고기, 과일들 참 많았고 맛있어 보였다. 대웅이가 어쩌면 내가 예전에 얘기했던 어떤 일을 하던 가족이 먼저라는 그걸 실천하려고 하는 건 아닐까라는 생각이 들었다. 어쩌면 정말 그럴 수도 있다. 대웅이한텐 그런 변화가 지금이고 지금 그런 변화가 시작되고 있는 걸 수도 있다. 그렇게 생각하니 또 기특한데 내가 생각만큼 리액션을 해주지 못한 것 같아서 미안하다. 주호를 재우고 우리의 저녁 식사를 준비했다.<br>- 19:00 - 21:00 저녁 메뉴는 대웅이가 가져온 안심을 맛있게 구워서 소고기를 해주었고, 장모님께서 회를 시켜주셨고, 한나는 아무도 먹지 않는 교촌치킨을 시켰다. 그렇게 저녁을 먹고 우리는 고스톱을 쳤는데 내가 집중이 잘 되지 않았다. 배도 아프기도 했고 화장실을 오가고 있었다.</p>\r\n<p>&nbsp;</p>\r\n<p>&nbsp;</p>	2025-02-07 00:00:00	2025-02-07 14:14:01.5058	1
18	ㄴㄹㅁㄴㅇㄹ	<p>ㅇㄹㅁㅇㄴㄹ</p>	2025-02-07 00:00:00	2025-02-07 14:17:29.583057	1
19	ㄴㅁㅇㄹㅁㅇㄹ	<p>ㄴㅇㄹㅇ</p>	2025-02-07 00:00:00	2025-02-07 14:17:57.553709	1
20	ㅁㄴㅇㄹㅇㄴㅁ	<p>ㄴㄹㅇㅁㄴㅇㄹ</p>	2025-02-07 00:00:00	2025-02-07 14:18:12.802769	1
21	ㅇㄹㅇㄹ	<p>ㄹㅇㄹ</p>	2025-02-07 00:00:00	2025-02-07 14:18:59.170242	1
22	ㅁㄴㅇㄹㅁㄴㅇㄹ	<p>ㅇㄹㅁㄴㅇㄹㅁㄴㄹ</p>	2025-02-07 00:00:00	2025-02-07 23:19:44.366417	1
23	ㅁㄴㅇㄹㅁㄴㄹㅇ	<p>ㄹㅁㄴㄹㅇ</p>	2025-02-18 00:00:00	2025-02-07 23:20:41.545693	1
24	ㅇㄹㅁㄴㄹㅁㅇㄴㄹ	<p>ㄹㅁㄴㄹㅁㄴㅇㄹ</p>	2025-03-11 00:00:00	2025-02-07 23:20:50.078617	1
25	우리아기	<p>ㅇㄹㅇㄹ</p>	2025-02-20 00:00:00	2025-02-07 23:32:56.060114	1
26	대표사진이 나온다?	<p>진짜로?</p>	2025-02-01 00:00:00	2025-02-07 23:34:15.258995	1
\.


--
-- Data for Name: diary_images; Type: TABLE DATA; Schema: public; Owner: jake
--

COPY public.diary_images (id, filename, diary_id, created_at, is_representative) FROM stdin;
6	c09f2ad0-392e-48ab-8f61-a709e2a85ea5_IMG_3159.jpg	7	2025-02-07 13:46:33.516059	f
8	448e601b-7d76-4b1f-b125-ccf78a2d561f_IMG_7554.JPG	8	2025-02-07 13:49:59.639392	f
9	4041511b-c526-406d-9701-08ec4a24a77b_IMG_7562.JPG	8	2025-02-07 13:49:59.639392	f
10	54a6df91-04cf-4be9-b9ed-dc4c36a69cb2_IMG_7563.JPG	8	2025-02-07 13:49:59.639392	f
11	5b354119-c6f7-41c2-aed0-a566183f53a2_IMG_7565.JPG	8	2025-02-07 13:49:59.639394	f
12	1390c95b-8322-4b3a-8d89-3778a8edac7f_IMG_7566.JPG	8	2025-02-07 13:49:59.639395	f
13	76939026-69df-4462-8259-04ce0fbedfda_IMG_7569.JPG	8	2025-02-07 13:49:59.639395	f
14	dac54834-f23e-4d81-a1bc-05d595e7b1ea_IMG_7609.JPG	8	2025-02-07 13:49:59.639396	f
15	d0a94c45-eb50-4698-a147-8268244da7a1_IMG_7610.JPG	8	2025-02-07 13:49:59.639396	f
17	a0969b05-3c78-4a59-88a3-429a392083ee.jpg	9	2025-02-07 13:59:40.287818	f
18	db652c84-c94e-4bc1-85bb-2452cb47418d.jpg	9	2025-02-07 13:59:40.28782	f
19	040ea850-ecd3-4d7a-a6bc-2f2a1bd2702d.jpg	9	2025-02-07 13:59:40.287821	f
20	8a2196da-ea9d-438e-a0c3-b213f727ced9.jpg	9	2025-02-07 13:59:40.287821	f
21	d3de3797-cec4-44b5-881b-bda3808e30e2.jpg	9	2025-02-07 13:59:40.287822	f
22	7c1cf48f-aa83-413c-aaae-23e462d75413.jpg	9	2025-02-07 13:59:40.287822	f
23	8d14face-c75c-48c9-91b2-949867b990a0.jpg	9	2025-02-07 13:59:40.287823	f
24	bbfa59e7-c514-4ea7-899b-2f65cb63361f.jpg	9	2025-02-07 13:59:40.287823	f
25	8d6bcc39-85e0-4424-b9fb-7dd67f532038.jpg	9	2025-02-07 13:59:40.287823	f
2	8022592d-860d-4718-862b-a56dd72a7ea5_IMG_3192.jpg	6	2025-02-07 13:44:39.327036	t
5	cb8fba59-76ac-431a-b783-e7d7c0715ab1_IMG_3156.jpg	7	2025-02-07 13:46:33.516053	t
7	e4f36f1e-65c1-43f2-b1b1-8de96a5b0faa_IMG_7611.JPG	8	2025-02-07 13:49:59.639385	t
16	079cab89-2250-4069-afe0-0493e48e12a4.jpg	9	2025-02-07 13:59:40.287814	t
26	89165cad-289c-4a35-a0aa-3677f43054d8.jpg	25	2025-02-07 14:32:56.077866	t
27	ced946c6-d29c-4a47-a5ec-f49cb574de1f.jpg	25	2025-02-07 14:32:56.07787	f
28	0dbf9c16-68a3-422f-80bc-c603eecb3d99.jpg	25	2025-02-07 14:32:56.077873	f
29	a1391069-4430-4461-bc0b-338b88c53ab2.jpg	25	2025-02-07 14:32:56.077873	f
30	2b0911be-8e60-4ea8-bb2e-86afea8c110b.jpg	26	2025-02-07 14:34:15.277362	f
31	9c00e102-4136-4577-94d0-7b68490a6c69.jpg	26	2025-02-07 14:34:15.277367	f
32	62ae2d4c-403c-4794-9e65-3bd162314ea2.jpg	26	2025-02-07 14:34:15.277368	f
33	1c2001de-119e-4f47-b97b-7e00a9bd8849.jpg	26	2025-02-07 14:34:15.277368	f
35	e64e8425-5e72-4f97-acd2-50c5753b9113.jpg	26	2025-02-07 14:34:15.277369	f
34	2406a218-5a39-4af4-bdf1-092174e152a2.jpg	26	2025-02-07 14:34:15.277368	t
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: jake
--

COPY public.users (id, username, password_hash, created_at, gpt_api_key_encrypted) FROM stdin;
1	jake10	scrypt:32768:8:1$m5oseB4ekt2zzmIW$26f70c5d7dff127b011993e0d74d8d0d41ea414104211c38a68a50bd2c5c305c8ec5e12d99af1d69af4dfcabb15330b0c52981e55c6560cd036c3554a020e2b8	2025-02-07 12:55:42.800712	\N
\.


--
-- Name: diaries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jake
--

SELECT pg_catalog.setval('public.diaries_id_seq', 26, true);


--
-- Name: diary_images_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jake
--

SELECT pg_catalog.setval('public.diary_images_id_seq', 35, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jake
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: jake
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: diaries diaries_pkey; Type: CONSTRAINT; Schema: public; Owner: jake
--

ALTER TABLE ONLY public.diaries
    ADD CONSTRAINT diaries_pkey PRIMARY KEY (id);


--
-- Name: diary_images diary_images_pkey; Type: CONSTRAINT; Schema: public; Owner: jake
--

ALTER TABLE ONLY public.diary_images
    ADD CONSTRAINT diary_images_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: jake
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: jake
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: diaries diaries_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jake
--

ALTER TABLE ONLY public.diaries
    ADD CONSTRAINT diaries_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: diary_images diary_images_diary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jake
--

ALTER TABLE ONLY public.diary_images
    ADD CONSTRAINT diary_images_diary_id_fkey FOREIGN KEY (diary_id) REFERENCES public.diaries(id);


--
-- PostgreSQL database dump complete
--



## 📖 Foydalanish qo'llanmasi

Sayt manzili: https://postflow-faxriddinswe-3378.up.railway.app/login-page


Loyihani o'z kompyuteringizga yuklab olish:

```bash
git clone https://github.com/faxriddinswe/PostFlow.git
cd PostFlow
```

### Virtual muhit (venv) yaratish

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

Terminalda `(venv)` yozuvi ko'rinsa — muvaffaqiyatli faollashgan.

---

## 📦 Kutubxonalarni o'rnatish

Loyihada barcha kerakli kutubxonalar `requirements.txt` faylida ro'yxatlangan. Bittasi bilan hammasini o'rnatish mumkin:

```bash
pip install -r requirements.txt
```

Agar `requirements.txt` bo'lmasa yoki qo'lda o'rnatmoqchi bo'lsangiz:

```bash
pip install fastapi uvicorn httpx python-dotenv sqlalchemy bcrypt python-jose "pydantic[email]" psycopg2-binary
```

Har bir kutubxona nima uchun kerakligi:

| Kutubxona | Vazifasi |
|---|---|
| `fastapi` | Backend framework — REST API |
| `uvicorn` | ASGI server — FastAPI'ni ishga tushiradi |
| `httpx` | Telegram Bot API bilan asinxron aloqa |
| `python-dotenv` | `.env` fayldan maxfiy sozlamalarni o'qish |
| `sqlalchemy` | ORM — database bilan Python orqali ishlash |
| `bcrypt` | Parollarni xavfsiz hash qilish |
| `python-jose` | JWT token yaratish/tekshirish |
| `pydantic[email]` | Kiruvchi ma'lumotni validatsiya qilish |
| `psycopg2-binary` | PostgreSQL bilan ulanish uchun drayver |

---

## 🤖 Telegram bot yaratish

1. Telegram'da **@BotFather**ni toping, `/start` bosing.
2. `/newbot` buyrug'ini yuboring, ism va username belgilang (username `bot` bilan tugashi shart).
3. BotFather sizga **API token** beradi — buni saqlab qo'ying.
4. Botingizni o'z Telegram kanalingizga **admin** qilib qo'shing (Kanal → Administrators → Add Admin → botni tanlang → "Post Messages" ruxsatini yoqing).

---

## 🔑 `.env` faylini sozlash

Loyiha papkasida `.env` nomli fayl yarating (boshida nuqta bilan):

```env
BOT_TOKEN=sizning_bot_tokeningiz
SECRET_KEY=juda_uzun_tasodifiy_maxfiy_kalit
```

`SECRET_KEY`ni tasodifiy generatsiya qilish:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

> ⚠️ `.env` fayli hech qachon Git'ga yuklanmasligi kerak — u `.gitignore`da bo'lishi shart (loyihada allaqachon sozlangan).

**Eslatma:** lokal ishga tushirishda `DATABASE_URL` kerak emas — loyiha standart holda `sqlite:///./app.db` ishlatadi. Bu faqat production (Railway/Render)da PostgreSQL uchun kerak bo'ladi.

---

## 🚀 Lokal ishga tushirish

```bash
uvicorn main:app --reload
```

Brauzerda oching:
http://127.0.0.1:8000

API dokumentatsiyasi (Swagger):
http://127.0.0.1:8000/docs

---

## ☁️ Production'ga deploy qilish (Railway)

1. [railway.com](https://railway.com) da GitHub orqali ro'yxatdan o'ting.
2. **New Project** → **Deploy from GitHub repo** → repositoriyangizni tanlang.
3. Service **Settings** → **Deploy** bo'limida Start Command'ni kiriting:
```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
```
4. **+ New** → **Database** → **Add PostgreSQL** orqali database qo'shing.
5. PostgreSQL'ning **Variables** bo'limidan `DATABASE_URL`ni nusxalang.
6. Web Service'ning **Variables** bo'limiga uchtasini qo'shing: `DATABASE_URL`, `BOT_TOKEN`, `SECRET_KEY`.
7. **Settings** → **Networking** → **Generate Domain** orqali ochiq manzil oling.

Kod database turidan mustaqil yozilgani uchun (SQLAlchemy ORM tufayli), lokal SQLite va production PostgreSQL orasida hech qanday qo'shimcha o'zgarish talab qilinmaydi — faqat `DATABASE_URL` muhit o'zgaruvchisi orqali avtomatik moslashadi.

---

## 📁 Loyiha strukturasi
PostFlow/
├── static/                 
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── founder.html
│   └── style.css
├── main.py                 
├── database.py             
├── models.py               
├── schemas.py              
├── auth.py                 
├── requirements.txt        
├── .gitignore             
└── README.md

---

## 📖 Foydalanish qo'llanmasi

1. **Ro'yxatdan o'ting** — ism, email, username, parol bilan.
2. **Botni kanalingizga admin qiling.**
3. **Login qiling**, Dashboard'da kanal username'ini kiritib **"Kanalni ulash"** bosing.
4. **Post yozing** — kerak bo'lsa Markdown bilan formatlashtiring (`**qalin**`, `*qiya*`, `` `kod` ``).
5. Qaysi kanalga yuborilishini tanlang, **Publish 🚀** bosing.
6. **Profil** bo'limida statistikangizni kuzating.

---

<p align="center">Made with ❤️ by Faxriddin</p>


### 1. Ro'yxatdan o'tish

Login sahifasidagi **"Ro'yxatdan o'tish"** linkini bosing, ism, email, username va parolni kiriting.

### 2. Botni kanalga admin qilish

O'zingizning Telegram kanalingizni oching → **Administrators** → **Add Admin** → yaratgan botingizni qidiring va admin sifatida qo'shing, **"Post Messages"** ruxsatini yoqing.

### 3. Kirish va kanal ulash

Username va parol bilan login qiling. Dashboard'da **"Telegram kanalni ulash"** bo'limiga kanal username'ini kiriting (masalan `@mening_kanalim`) va **"Kanalni ulash"** tugmasini bosing. Tizim avtomatik tekshiradi: bot haqiqatan shu kanalda adminmi.

### 4. Post yozish va yuborish

"Post yozish" bo'limida matningizni yozing. Kerak bo'lsa, toolbar tugmalari yordamida formatlashtiring:

| Tugma | Natija | Misol |
|---|---|---|
| **B** | Qalin matn | `**muhim**` → **muhim** |
| *I* | Qiya matn | `*eslatma*` → _eslatma_ |
| `{ }` | Inline kod | `` `kod` `` → `kod` |
| `{ ;;; }` | Kod bloki | ` ```kod bloki``` ` |
| ❝❞ | Iqtibos | `> aytilgan gap` |

**Publish 🚀** tugmasini bosing — post darhol ulangan Telegram kanalingizga yuboriladi.

### 5. Profil va faollik

Navbardagi **Profil** bo'limida jami yuborilgan postlar soni, faol kunlar soni va GitHub uslubidagi yillik faollik grafigini ko'rishingiz mumkin.

---

## 🔌 API endpoint'lar ro'yxati

| Method | Endpoint | Himoyalanganmi | Vazifasi |
|---|---|:---:|---|
| `POST` | `/register` | ✅  | Yangi foydalanuvchi ro'yxatdan o'tkazish |
| `POST` | `/login` | ✅  | Login qilish, JWT token olish |
| `POST` | `/channels/connect` | ✅ | Telegram kanalni ulash |
| `POST` | `/publish` | ✅ | Post yozish va Telegram kanalga yuborish |
| `GET` | `/profile/data` | ✅ | Foydalanuvchi statistikasi va faollik tarixi |
| `GET` | `/` `/login-page` `/register-page` `/dashboard` `/profile-page` `/founder-page` | — | Frontend HTML sahifalarni qaytaradi |

✅ = so'rov header'ida `Authorization: Bearer <token>` talab qilinadi.

---

## 🛡 Xavfsizlik

Loyihada quyidagi xavfsizlik tamoyillari amalga oshirilgan:

- **Parollar hech qachon ochiq matnda saqlanmaydi** — `bcrypt` algoritmi bilan bir tomonlama hash qilinadi, orqaga qaytarib bo'lmaydi.
- **JWT token orqali autentifikatsiya** — har bir himoyalangan so'rov imzolangan tokenni talab qiladi, token muddati 24 soatdan keyin tugaydi.
- **Maxfiy kalitlar `.env` faylida** — hech qachon kod ichida yoki repozitoriyda ochiq saqlanmaydi.
- **Egalik huquqi tekshiruvi (Object-Level Authorization)** — bitta Telegram kanal faqat bitta foydalanuvchiga tegishli bo'lishi mumkin; boshqa foydalanuvchi allaqachon ulangan kanalni o'zlashtira olmaydi. Bu tekshiruv ham kod darajasida, ham database darajasida (`unique` cheklov) amalga oshirilgan.
- **HTML escaping** — foydalanuvchi kiritgan matndagi `<`, `>`, `&` belgilari Telegram'ga yuborishdan oldin xavfsiz shaklga o'giriladi, bu formatlash xatolarining va zararli kodning oldini oladi.
- **Bir xil xato xabari** — login muvaffaqiyatsiz bo'lganda, tizim "username topilmadi" va "parol noto'g'ri"ni alohida ajratmaydi, bu orqali tashqi tomondan qaysi username'lar mavjudligini aniqlash imkoniyati yo'qoladi.

---

## ✍️ Markdown formatlash

PostFlow foydalanuvchi yozgan oddiy Markdown belgilarini backend tomonida Telegram tushunadigan HTML formatiga avtomatik o'giradi:

| Markdown | Telegram HTML | Ko'rinishi |
|---|---|---|
| `**matn**` | `<b>matn</b>` | **qalin** |
| `*matn*` | `<i>matn</i>` | _qiya_ |
| `` `matn` `` | `<code>matn</code>` | `kod` |
| ` ```matn``` ` | `<pre>matn</pre>` | kod bloki |
| `> matn` | `<blockquote>matn</blockquote>` | iqtibos |

Konvertatsiya `main.py` ichidagi `markdown_to_telegram_html()` funksiyasida regex (`re` moduli) yordamida amalga oshiriladi.

---

## 🔧 Muammolarni bartaraf etish

**`chat not found` xatosi** — `.env` yoki database'dagi kanal username'i noto'g'ri. Kanal `@` belgisi bilan, to'g'ri username'da ekanligiga ishonch hosil qiling.

**`bot is not a member` / `403` xatosi** — Bot hali kanalga admin qilib qo'shilmagan. Kanal sozlamalari → Administrators → botni qo'shing.

**`ConnectTimeout` xatosi** — internet aloqasi yoki Telegram serveriga ulanishda vaqtinchalik muammo. Bir necha soniyadan keyin qayta urinib ko'ring.

**`IndentationError` yoki `ImportError`** — Python kod faylida chekinish (bo'sh joy) yoki import xatosi. Terminal'dagi to'liq xato matnini (traceback) o'qib, ko'rsatilgan qator raqamiga qarang.

**`404 Not Found` (`/static/style.css`)** — `main.py`da `app.mount("/static", StaticFiles(directory="static"), name="static")` qatori borligini tekshiring.

---

## 🗺 Kelajakdagi rejalar

- [ ] Blog integratsiyasi — bitta postni Telegram bilan bir vaqtda statik blog saytiga (GitHub API orqali) ham chiqarish
- [ ] Rasm va media fayllarni postlarga qo'shish imkoniyati
- [ ] Postlarni rejalashtirilgan vaqtda avtomatik yuborish (scheduled posting)
- [ ] PostgreSQL'ga o'tish (SQLite'dan) — ko'p foydalanuvchili yuklama uchun
- [ ] Alembic orqali database migratsiyalarini boshqarish
- [ ] Docker konteynerlashtirish va production deploy

---

## 👤 Muallif

**Faxriddin Baxtiyorov** — Backend Engineering yo'nalishida o'zini rivojlantirayotgan dasturchi.

Ushbu loyiha — FastAPI, autentifikatsiya, database dizayni va xavfsizlik tamoyillarini amaliyotda chuqur o'rganish maqsadida, nol darajadan qadamma-qadam qurilgan.


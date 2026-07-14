Bu yerda har bir endpoint'ni to'g'ridan-to'g'ri brauzerdan sinab ko'rish mumkin.

---

## 📖 Foydalanish qo'llanmasi

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
| `POST` | `/register` | ❌ | Yangi foydalanuvchi ro'yxatdan o'tkazish |
| `POST` | `/login` | ❌ | Login qilish, JWT token olish |
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

**Faxriddin** — Backend Engineering yo'nalishida o'zini rivojlantirayotgan dasturchi.

Ushbu loyiha — FastAPI, autentifikatsiya, database dizayni va xavfsizlik tamoyillarini amaliyotda chuqur o'rganish maqsadida, nol darajadan qadamma-qadam qurilgan.

---

<p align="center">Made with ❤️ and a lot of debugging.</p>
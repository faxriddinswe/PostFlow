import os                          # operatsion tizim bilan ishlash (env o'qish uchun)
import httpx                       # HTTP so'rovlar yuborish uchun (async)
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel     # kelayotgan ma'lumotni tekshirish uchun
from dotenv import load_dotenv     # .env faylni o'qish
import re
from database import engine, Base
import models

from sqlalchemy.orm import Session
from fastapi import Depends

from database import get_db
from auth import hash_password
from models import User, Channel
from schemas import UserCreate, UserLogin, ChannelCreate
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)


from auth import hash_password, verify_password, create_access_token
from schemas import UserCreate, UserLogin

from models import User, Channel, Post

from schemas import UserCreate, UserLogin, ChannelCreate, PostCreate

load_dotenv()  # .env fayldagi qiymatlarni yuklaydi

BOT_TOKEN = os.getenv("BOT_TOKEN")      # .env dan tokenni olamiz
CHANNEL_ID = os.getenv("CHANNEL_ID")    # .env dan kanal nomini olamiz

app = FastAPI()  # bizning web-dasturimiz



def markdown_to_telegram_html(text: str) -> str:
    """
    Foydalanuvchi yozgan oddiy Markdown belgilarini Telegram HTML formatiga o'giradi.
    Tartib muhim: avval kod bloklari, keyin qalin/qiya, oxirida iqtibos.
    """
    # 1. Avval xavfli HTML belgilarni "xavfsiz" qilib olamiz (escaping)
    #    Bu -- foydalanuvchi tasodifan < yoki > yozib qo'ysa, Telegram xato bermasligi uchun
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # 2. Kod bloki: ```matn``` -> <pre>matn</pre>
    #    re.DOTALL -- "." belgisi yangi qatorni ham qamrab olishini ta'minlaydi
    text = re.sub(r"```(.+?)```", r"<pre>\1</pre>", text, flags=re.DOTALL)

    # 3. Qalin: **matn** -> <b>matn</b>
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)

    # 4. Qiya: *matn* -> <i>matn</i>
    #    Diqqat: bu qadam qalin (**) dan KEYIN bo'lishi shart, aks holda **qalin**ni buzib qo'yadi
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)

    # 5. Inline kod: `matn` -> <code>matn</code>
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)

    # 6. Iqtibos: qator boshida "> " bilan boshlangan har bir qatorni topamiz
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        if line.startswith("&gt; "):  # chunki > allaqachon &gt;ga aylangan (1-qadamda)
            new_lines.append(f"<blockquote>{line[5:]}</blockquote>")
        else:
            new_lines.append(line)
    text = "\n".join(new_lines)

    return text


async def check_bot_is_admin(channel_username: str) -> bool:
    """
    Telegram'dan so'raymiz: bizning bot shu kanalda a'zomi, va u admin/creator'mi?
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"

    # Bizning botimizning o'z user_id'sini olishimiz kerak -- getMe orqali
    async with httpx.AsyncClient() as client:
        me_resp = await client.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getMe")
        me_data = me_resp.json()
        if not me_data.get("ok"):
            return False
        bot_id = me_data["result"]["id"]

        # Endi shu kanalda bot qanday rolda ekanini so'raymiz
        resp = await client.get(url, params={
            "chat_id": channel_username,
            "user_id": bot_id,
        })
        data = resp.json()

        if not data.get("ok"):
            return False

        status_in_chat = data["result"]["status"]
        # Telegram status'lari: "creator", "administrator", "member", "left", "kicked"
        return status_in_chat in ("administrator", "creator")

# Dastur ishga tushganda, models.py'da tavsiflangan jadvallarni database'da yaratadi
# (agar ular hali mavjud bo'lmasa)
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
# Frontend'dan keladigan ma'lumot shakli:
# { "text": "post matni" } bo'lishi shart, bo'lmasa FastAPI o'zi xato qaytaradi


@app.post("/publish")
async def publish(post: PostCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not post.text.strip():
        raise HTTPException(status_code=400, detail="Post bo'sh bo'lmasligi kerak")

    # MUHIM: shu channel_id bo'yicha qidiramiz, VA u shu userga tegishli ekanini tekshiramiz.
    # Ikkinchi shart (user_id == current_user.id) bo'lmasa, boshqa userning kanal_id'sini
    # tахmin qilib, unga post yuborib yuborish mumkin bo'lardi -- yana bir egalik tekshiruvi!
    channel = db.query(Channel).filter(
        Channel.id == post.channel_id,
        Channel.user_id == current_user.id,
    ).first()

    if not channel:
        raise HTTPException(status_code=404, detail="Kanal topilmadi yoki sizga tegishli emas")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json={
                "chat_id": channel.channel_username,
                "text": markdown_to_telegram_html(post.text),
                "parse_mode": "HTML",
            })
    except httpx.ConnectTimeout:
        raise HTTPException(
            status_code=504,
            detail="Telegram serveriga ulanib bo'lmadi. Internet aloqangizni tekshiring va qayta urinib ko'ring.",
        )

    data = response.json()
    if not data.get("ok"):
        raise HTTPException(status_code=500, detail=data.get("description"))

    new_post = Post(user_id=current_user.id)
    db.add(new_post)
    db.commit()

    return {"status": "success", "message": f"Post {channel.channel_username} kanaliga yuborildi!"}

# Bosh sahifa: editor'ni ko'rsatamiz
@app.get("/")
async def home():
    # Bosh sahifa endi to'g'ridan-to'g'ri login'ga yo'naltiradi
    return FileResponse("static/login.html")


@app.get("/login-page")
async def login_page():
    return FileResponse("static/login.html")


@app.get("/register-page")
async def register_page():
    return FileResponse("static/register.html")


@app.get("/dashboard")
async def dashboard_page():
    return FileResponse("static/dashboard.html")

@app.get("/profile-page")
async def profile_page():
    return FileResponse("static/profile.html")


@app.get("/founder-page")
async def founder_page():
    return FileResponse("static/founder.html")


@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Bu email allaqachon ro'yxatdan o'tgan")

    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Bu username band")

    new_user = User(
        name=user.name,
        email=user.email,
        username=user.username,
        password_hash=hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "status": "success",
        "message": f"Xush kelibsiz, {new_user.name}! Ro'yxatdan muvaffaqiyatli o'tdingiz.",
        "user_id": new_user.id,
    }


@app.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Username yoki parol noto'g'ri")

    access_token = create_access_token(data={"sub": user.username, "user_id": user.id})

    return {
        "status": "success",
        "access_token": access_token,
        "token_type": "bearer",
    }


@app.post("/channels/connect")
async def connect_channel(
    channel: ChannelCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    is_admin = await check_bot_is_admin(channel.channel_username)

    if not is_admin:
        raise HTTPException(
            status_code=400,
            detail="Bot bu kanalda admin emas. Avval botni kanalingizga admin qilib qo'shing.",
        )

    # MUHIM: bu kanal HAR QANDAY user tomonidan allaqachon ulanganmi -- tekshiramiz.
    # user_id bo'yicha emas, faqat channel_username bo'yicha qidiramiz.
    already_taken = db.query(Channel).filter(
        Channel.channel_username == channel.channel_username
    ).first()

    if already_taken:
        if already_taken.user_id == current_user.id:
            raise HTTPException(status_code=400, detail="Siz bu kanalni allaqachon ulagansiz")
        else:
            raise HTTPException(
                status_code=403,
                detail="Bu kanal sizniki emas -- boshqa foydalanuvchi tomonidan allaqachon ulangan",
            )

    new_channel = Channel(
        user_id=current_user.id,
        channel_username=channel.channel_username,
        is_verified=True,
    )
    db.add(new_channel)
    db.commit()
    db.refresh(new_channel)

    return {
        "status": "success",
        "message": f"{channel.channel_username} muvaffaqiyatli ulandi!",
        "channel_id": new_channel.id,
    }


@app.get("/channels")
def list_channels(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    channels = db.query(Channel).filter(Channel.user_id == current_user.id).all()
    return [
        {"id": c.id, "channel_username": c.channel_username}
        for c in channels
    ]


@app.delete("/channels/{channel_id}")
def delete_channel(channel_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # MUHIM: bu yerda ham egalik tekshiruvi -- faqat O'ZINING kanalini o'chira oladi
    channel = db.query(Channel).filter(
        Channel.id == channel_id,
        Channel.user_id == current_user.id,
    ).first()

    if not channel:
        raise HTTPException(status_code=404, detail="Kanal topilmadi yoki sizga tegishli emas")

    db.delete(channel)
    db.commit()

    return {"status": "success", "message": f"{channel.channel_username} o'chirildi"}

@app.get("/profile/data")
def get_profile_data(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.user_id == current_user.id).all()

    # Har bir kunda nechta post yozilganini sanaymiz
    # Masalan: {"2026-07-14": 3, "2026-07-13": 1}
    activity = {}
    for p in posts:
        day = p.created_at.date().isoformat()
        activity[day] = activity.get(day, 0) + 1

    return {
        "name": current_user.name,
        "username": current_user.username,
        "member_since": current_user.created_at.date().isoformat(),
        "total_posts": len(posts),
        "active_days": len(activity),
        "activity": activity,
    }
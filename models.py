from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from database import Base

# Bu klass -- "users" jadvalining Python'dagi ko'rinishi.
# Har bir Column -- jadvaldagi bitta ustun (column).
class User(Base):
    __tablename__ = "users"   # database'dagi jadval nomi

    id = Column(Integer, primary_key=True, index=True)
    # primary_key=True -- bu ustun har bir qatorni noyob aniqlaydi (unique ID)
    # index=True -- qidirishni tezlashtiradi

    name = Column(String, nullable=False)
    # nullable=False -- bu maydon bo'sh bo'lishi mumkin emas, majburiy

    email = Column(String, unique=True, index=True, nullable=False)
    # unique=True -- ikkita user bir xil email bilan ro'yxatdan o'ta olmaydi

    username = Column(String, unique=True, index=True, nullable=False)
    # unique=True -- ikkita user bir xil username ololmaydi

    password_hash = Column(String, nullable=False)
    # DIQQAT: parolning o'zi emas, uning HASH'i saqlanadi (3-darsda tushuntiraman)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # server_default=func.now() -- yangi user qo'shilganda vaqt avtomatik yoziladi


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # ForeignKey -- "bu kanal aynan shu user_id'ga tegishli" degan bog'lanish.
    # Bu relational database'larning yuragi: ikkita jadvalni bog'laydi.

    channel_username = Column(String, nullable=False, unique=True)
    # Masalan: "@mening_kanalim"

    is_verified = Column(Boolean, default=False)
    # Bot shu kanalda admin ekanini tekshirganimizdan keyin True bo'ladi

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # Postning matnini saqlash shart emas (Telegram'da allaqachon bor),
    # bizga faqat "qachon yuborilgani" kerak -- faollik grafigi uchun
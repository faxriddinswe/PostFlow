from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database manzili. sqlite:/// -- SQLite ekanini bildiradi.
# "app.db" -- loyiha papkasida shu nomli fayl yaratiladi, o'sha yerda hamma
# ma'lumotlar saqlanadi.
DATABASE_URL = "sqlite:///./app.db"

# engine -- database bilan "aloqa liniyasi". Har bir so'rov shu orqali ketadi.
# check_same_thread=False -- SQLite'ga xos sozlama, FastAPI bilan ishlashi uchun kerak.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal -- database bilan "suhbat" ochish uchun fabrika (factory).
# Har bir HTTP so'rov kelganda, bitta yangi "session" ochamiz, ish tugagach yopamiz.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base -- bizning barcha jadval-klasslarimiz shundan meros oladi (inherit).
# Bu SQLAlchemy'ga "bu klass jadvalga aylanadi" deb aytadi.
Base = declarative_base()


def get_db():
    """
    Har bir HTTP so'rov uchun database session ochadi,
    ish tugagach (yield'dan keyin) avtomatik yopadi.
    Bu FastAPI'ning "Dependency Injection" mexanizmi -- keyinroq chuqurroq tushuntiraman.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
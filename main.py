from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import auth, event, task

# Import semua model agar SQLAlchemy bisa membuat tabel
from models import User, Event, Task  # noqa: F401

# ============================================================
# Inisialisasi Aplikasi
# ============================================================
app = FastAPI(
    title="API Manajemen Kepanitiaan Kampus",
    description="""
## 🎓 Sistem Manajemen Kegiatan Kepanitiaan Kampus

API ini menyediakan fitur untuk mengelola kegiatan dan tugas kepanitiaan kampus.

### Fitur Utama:
-  Autentikasi: Registrasi & login dengan JWT token
-  Manajemen Event: CRUD event/kegiatan kepanitiaan
-  Manajemen Task: CRUD tugas kepanitiaan dengan status tracking
-  Relasi: Event memiliki banyak Task (One-to-Many)

### Cara Penggunaan:
1. **Register** akun baru di `/auth/register`
2. **Login** di `/auth/login` untuk mendapatkan token JWT
3. Klik tombol **Authorize**  di atas dan masukkan token
4. Gunakan endpoint yang tersedia untuk mengelola event & task
    """,
    version="1.0.0",
    contact={
        "name": "Mahasiswa Pemrograman Web Lanjutan",
    },
)

# ============================================================
# CORS Middleware
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Buat Tabel Database
# ============================================================
Base.metadata.create_all(bind=engine)

# ============================================================
# Daftarkan Router
# ============================================================
app.include_router(auth.router)
app.include_router(event.router)
app.include_router(task.router)


# ============================================================
# Root Endpoint
# ============================================================
@app.get("/", tags=["Root"])
def root():
    """Endpoint root — informasi dasar API."""
    return {
        "message": "Selamat datang di API Manajemen Kepanitiaan Kampus!",
        "docs": "/docs",
        "version": "1.0.0"
    }

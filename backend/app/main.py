from __future__ import annotations
import os
import uuid
from typing import List
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from .database import Base, engine, get_db
from .models import File as FileModel
from .schemas import FileRead
from .storage import LocalStorage, S3Storage, StorageBackend
from .utils import categorize, extract_metadata

load_dotenv()

# Garante que o diretório exista para StaticFiles no modo local
os.makedirs("uploads", exist_ok=True)

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gerenciador de Arquivos API", version="1.0.0")

# CORS
cors_origins = os.getenv("CORS_ORIGINS", "")
if cors_origins.strip():
    origins = [o.strip() for o in cors_origins.split(",") if o.strip()]
else:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage backend
storage_backend: StorageBackend
backend_kind = os.getenv("STORAGE_BACKEND", "local").lower()
if backend_kind == "s3":
    bucket = os.getenv("S3_BUCKET")
    region = os.getenv("S3_REGION", "us-east-1")
    key = os.getenv("AWS_ACCESS_KEY_ID")
    secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not all([bucket, region, key, secret]):
        raise RuntimeError("S3 configuration is incomplete. Check environment variables.")
    storage_backend = S3Storage(bucket=bucket, region=region, aws_access_key_id=key, aws_secret_access_key=secret)
else:
    storage_backend = LocalStorage(base_dir="uploads", base_url="/uploads")
    # Serve local uploads (only if using LocalStorage)
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/files", response_model=List[FileRead])
def list_files(db: Session = Depends(get_db)):
    items = db.query(FileModel).order_by(FileModel.created_at.desc()).all()
    return items

@app.get("/api/files/{file_id}", response_model=FileRead)
def get_file(file_id: int, db: Session = Depends(get_db)):
    f = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not f:
        raise HTTPException(status_code=404, detail="File not found")
    return f

@app.post("/api/upload", response_model=List[FileRead])
async def upload_files(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    for upload in files:
        original_name = upload.filename or "file.bin"
        ext = os.path.splitext(original_name)[1].lower()
        safe_name = original_name.replace("/", "_").replace("\\", "_")
        unique_name = f"{uuid.uuid4().hex}{ext}"
        mime = upload.content_type or "application/octet-stream"

        # Save to storage
        file_url = storage_backend.save(upload, unique_name)

        # Compute metadata/size if local
        file_size = 0
        width = height = pages = None
        duration = None

        if isinstance(storage_backend, LocalStorage):
            local_path = os.path.join("uploads", unique_name)
            try:
                file_size = os.path.getsize(local_path)
            except Exception:
                file_size = 0
            width, height, duration, pages = extract_metadata(local_path, mime)
        else:
            # Em S3, metadados podem exigir head_object/chamadas extras (opcional)
            pass

        category = categorize(mime)

        file_rec = FileModel(
            name=safe_name,
            file_url=file_url,
            file_size=file_size,
            file_type=mime,
            category=category,
            width=width,
            height=height,
            duration=duration,
            pages=pages,
        )
        db.add(file_rec)

    db.commit()

    # Retorna a lista completa (ou poderia retornar apenas os novos criados)
    all_items = db.query(FileModel).order_by(FileModel.created_at.desc()).all()
    return all_items
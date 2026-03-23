from __future__ import annotations
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    file_url = Column(String(100), nullable=False)
    file_size = Column(Integer, nullable=False, default=0)
    file_type = Column(String(100), nullable=False)  # MIME type
    category = Column(String(8), nullable=False)   # image, document, audio, video, other
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    duration = Column(Float, nullable=True)     # seconds for audio/video
    pages = Column(Integer, nullable=True)      # for PDFs
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

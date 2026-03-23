from __future__ import annotations
from typing import Optional, Tuple
import os
from PIL import Image
from mutagen import File as MutagenFile
from PyPDF2 import PdfReader

def categorize(mime: str) -> str:
    if not mime:
        return "other"
    if mime.startswith("image/"):
        return "image"
    if mime.startswith("audio/"):
        return "audio"
    if mime.startswith("video/"):
        return "video"
    if mime in (
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-powerpoint",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "text/plain",
    ):
        return "document"
    return "document" if "application/" in mime else "other"

def extract_metadata(file_path: str, mime: str) -> Tuple[Optional[int], Optional[int], Optional[float], Optional[int]]:
    """Return (width, height, duration, pages)."""
    width = height = pages = None
    duration = None

    try:
        if mime.startswith("image/"):
            with Image.open(file_path) as img:
                width, height = img.size
        elif mime == "application/pdf":
            with open(file_path, "rb") as f:
                reader = PdfReader(f)
                pages = len(reader.pages)
        elif mime.startswith("audio/") or mime.startswith("video/"):
            try:
                mf = MutagenFile(file_path)
                if mf and mf.info:
                    duration = float(getattr(mf.info, "length", None)) if hasattr(mf.info, "length") else None
            except Exception:
                pass
    except Exception:
        # Best effort; ignore errors
        pass

    return width, height, duration, pages

from __future__ import annotations
import os
import uuid
from typing import Tuple
from fastapi import UploadFile
from starlette.datastructures import UploadFile as StarletteUploadFile

class StorageBackend:
    def save(self, upload: UploadFile, dest_name: str) -> str:
        raise NotImplementedError

class LocalStorage(StorageBackend):
    def __init__(self, base_dir: str = "uploads", base_url: str = "/uploads"):
        self.base_dir = base_dir
        self.base_url = base_url
        os.makedirs(self.base_dir, exist_ok=True)

    def save(self, upload: UploadFile, dest_name: str) -> str:
        # Ensure safe filename
        filename = dest_name
        full_path = os.path.join(self.base_dir, filename)

        with open(full_path, "wb") as f:
            while True:
                chunk = upload.file.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)

        return f"{self.base_url}/{filename}"

class S3Storage(StorageBackend):
    def __init__(self, bucket: str, region: str, aws_access_key_id: str, aws_secret_access_key: str):
        import boto3
        self.bucket = bucket
        self.region = region
        self.s3 = boto3.client(
            "s3",
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def save(self, upload: UploadFile, dest_name: str) -> str:
        # Upload to S3
        self.s3.upload_fileobj(upload.file, self.bucket, dest_name, ExtraArgs={"ContentType": upload.content_type})
        # Public URL pattern may vary depending on bucket policy/CDN
        return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{dest_name}"

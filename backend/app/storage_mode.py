import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from flask import current_app

BASE_DIR = os.getcwd()
local_storage_folder_name = "uploads"
LOCAL_UPLOAD_FOLDER = os.path.join(BASE_DIR, local_storage_folder_name)

def upload_file(file):
    if current_app.config["STORAGE_MODE"] == "local":
        os.makedirs(LOCAL_UPLOAD_FOLDER, exist_ok = True)
        path = os.path.join(local_storage_folder_name, file.filename)
        file.save(path)
        return path
    
    elif current_app.config["STORAGE_MODE"] == "s3":
        s3 = boto3.client(
            "s3",
            aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"],
            region_name=current_app.config["AWS_REGION"],
        )
        try:
            s3.upload_fileobj(
                file,
                current_app.config["AWS_BUCKET"],
                file.filename
            )

            return f"https://{current_app.config['AWS_BUCKET']}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/{file.filename}"
        
        except (BotoCoreError, ClientError) as e:
            raise Exception(f"S3 upload failed: {str(e)}")

    else:
        raise ValueError("Invalid STORAGE_MODE. Use 'local' or 's3'.")

def delete_file(filename):
    if current_app.config["STORAGE_MODE"] == "local":
        path = os.path.join(local_storage_folder_name, filename)
        if os.path.exists(path):
            os.remove(path)

    elif current_app.config["STORAGE_MODE"] == "s3":
        s3 = boto3.client(
            "s3",
            aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"],
            region_name=current_app.config["AWS_REGION"],
        )

        try:
            s3.delete_object(
                Bucket=current_app.config["AWS_BUCKET"],
                Key=filename
            )
        
        except (BotoCoreError, ClientError) as e:
            raise Exception(f"S3 delete failed : {str(e)}")

    else:
        raise ValueError("Invalid STORAGE_MODE. Use 'local' or 's3'.")
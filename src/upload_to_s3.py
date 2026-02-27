import boto3
import os
from dotenv import load_dotenv
from utils.logger import setup_logger

load_dotenv()
logger = setup_logger("S3_Uploader")

def upload_file(file_name):
    bucket = os.getenv("S3_BUCKET_NAME")
    region = os.getenv("AWS_REGION")
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    s3 = boto3.client(
        "s3",
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    try:
        s3.upload_file(file_name, bucket, os.path.basename(file_name))
        logger.info(f"✅ Successfully uploaded {file_name} to {bucket}")
    except Exception as e:
        logger.error(f"❌ S3 Upload failed: {e}")

if __name__ == "__main__":
    path = "data/processed/cleaned_epl_2025_2026.csv"
    upload_file(path)
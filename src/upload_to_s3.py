import boto3
import os
from dotenv import load_dotenv
from utils.logger import setup_logger

load_dotenv()
logger = setup_logger("S3_Uploader")

def upload_to_s3():
    # 1. Define the path to the cleaned file
    # Make sure this matches the output_file name in cleaning.py exactly!
    local_file = os.path.join("data", "processed", "cleaned_epl_2025_2026.csv")
    
    bucket_name = os.getenv("S3_BUCKET_NAME")
    s3_object_name = "epl_data/latest_stats.csv"

    # 2. Check if the file actually exists before trying to upload
    if not os.path.exists(local_file):
        logger.error(f"❌ File not found: {local_file}. Did the cleaning step fail?")
        return False

    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION")
    )

    try:
        logger.info(f"📤 Uploading {local_file} to S3...")
        s3_client.upload_file(local_file, bucket_name, s3_object_name)
        logger.info("✅ Upload Successful!")
        return True
    except Exception as e:
        logger.error(f"❌ S3 Upload failed: {e}")
        return False
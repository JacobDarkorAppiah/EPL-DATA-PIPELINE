import boto3
import os
from dotenv import load_dotenv
from utils.logger import setup_logger

# Load local .env for local testing; GitHub will use Repository Secrets
load_dotenv()
logger = setup_logger("S3_Uploader")

def upload_to_s3():
    # 1. MATCH THE PATH: Must be identical to output_file in cleaning.py
    local_file = os.path.join("data", "processed", "cleaned_epl_2025_2026.csv")
    
    # 2. Get credentials from environment (GitHub Secrets)
    bucket_name = os.getenv("S3_BUCKET_NAME")
    s3_object_name = "epl_data/latest_stats.csv"  # The name it will have in AWS

    # 3. Pre-flight check: Does the file exist?
    if not os.path.exists(local_file):
        logger.error(f"❌ Upload aborted: The file {local_file} does not exist. Check if cleaning.py ran successfully.")
        return False

    # 4. Initialize Boto3 Client
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION")
        )

        logger.info(f"📤 Uploading {local_file} to S3 bucket: {bucket_name}...")
        
        # 5. Perform the Upload
        s3_client.upload_file(local_file, bucket_name, s3_object_name)
        
        logger.info(f"✅ Upload Successful! File available at: s3://{bucket_name}/{s3_object_name}")
        return True

    except Exception as e:
        logger.error(f"❌ S3 Upload failed: {str(e)}")
        return False

if __name__ == "__main__":
    upload_to_s3()
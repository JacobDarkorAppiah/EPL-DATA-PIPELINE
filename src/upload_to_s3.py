import boto3
import os
from dotenv import load_dotenv
from utils.logger import setup_logger

# Load local .env for local testing; GitHub will use Repository Secrets
load_dotenv()
logger = setup_logger("S3_Uploader")

def upload_to_s3():
    # 1. MATCH THE PATH: Using os.path.join for Linux/Windows compatibility
    local_file = os.path.join("data", "processed", "cleaned_epl_2025_2026.csv")
    
    # 2. Get credentials and validate they exist
    bucket_name = os.getenv("S3_BUCKET_NAME")
    s3_object_name = "epl_data/latest_stats.csv"
    
    # Check if critical variables are missing
    if not all([os.getenv("AWS_ACCESS_KEY_ID"), os.getenv("AWS_SECRET_ACCESS_KEY"), bucket_name]):
        logger.error("❌ S3 Credentials or Bucket Name missing from environment variables.")
        return False

    # 3. Pre-flight check: Does the file exist?
    if not os.path.exists(local_file):
        logger.error(f"❌ Upload aborted: {local_file} not found. Ensure cleaning.py ran successfully.")
        return False

    # 4. Initialize Boto3 Client
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1") # Default to us-east-1 if not set
        )

        logger.info(f"📤 Uploading {local_file} to S3 bucket: {bucket_name}...")
        
        # 5. Perform the Upload with Metadata
        # Adding 'ContentType' ensures the file isn't treated as a generic 'binary' file
        s3_client.upload_file(
            local_file, 
            bucket_name, 
            s3_object_name,
            ExtraArgs={'ContentType': 'text/csv'}
        )
        
        logger.info(f"✅ Upload Successful! Destination: s3://{bucket_name}/{s3_object_name}")
        return True

    except Exception as e:
        logger.error(f"❌ S3 Upload failed: {str(e)}")
        return False

if __name__ == "__main__":
    upload_to_s3()
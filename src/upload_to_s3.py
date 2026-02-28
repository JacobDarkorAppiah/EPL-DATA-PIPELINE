import boto3
import os
from dotenv import load_dotenv
from utils.logger import setup_logger

# Load local .env for local testing; GitHub will use Repository Secrets
load_dotenv()
logger = setup_logger("S3_Uploader")

def upload_to_s3():
    # 1. Path Consistency: Must match cleaning.py output
    local_file = os.path.join("data", "processed", "cleaned_epl_2025_2026.csv")
    
    # 2. Extract and Validate Environment Variables
    bucket_name = os.getenv("S3_BUCKET_NAME")
    s3_object_name = "epl_data/latest_stats.csv"
    
    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not all([aws_key, aws_secret, bucket_name]):
        logger.error("❌ Critical Error: AWS Credentials or Bucket Name missing from Environment!")
        return False

    # 3. Pre-flight check: Does the file exist?
    if not os.path.exists(local_file):
        logger.error(f"❌ Upload aborted: {local_file} not found. Scraper likely blocked by 403.")
        return False

    # 4. Initialize Client and Upload
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret,
            region_name=aws_region
        )

        logger.info(f"📤 Uploading to S3: {bucket_name}/{s3_object_name}...")
        
        # Adding ContentType ensures the file opens correctly in browsers/apps
        s3_client.upload_file(
            local_file, 
            bucket_name, 
            s3_object_name,
            ExtraArgs={'ContentType': 'text/csv'}
        )
        
        logger.info("✅ Upload Successful!")
        return True

    except Exception as e:
        logger.error(f"❌ S3 Client Error: {str(e)}")
        return False

if __name__ == "__main__":
    upload_to_s3()
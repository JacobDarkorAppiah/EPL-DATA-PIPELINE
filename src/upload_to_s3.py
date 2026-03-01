import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def upload_file():
    s3 = boto3.client('s3')
    bucket = os.getenv("S3_BUCKET_NAME")
    file_path = "data/processed/epl_standings.csv"
    object_name = "gold/epl_standings.csv" # Organizing it in a 'gold' folder

    try:
        s3.upload_file(file_path, bucket, object_name)
        print(f"🚀 Success! {file_path} is now in s3://{bucket}/{object_name}")
    except Exception as e:
        print(f"❌ Upload failed: {e}")

if __name__ == "__main__":
    upload_file()
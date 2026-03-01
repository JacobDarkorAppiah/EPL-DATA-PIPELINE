import boto3
import os

# Use the same bucket name you set in your secrets
BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'epl-data-lake-jacob')

def verify_s3_content():
    try:
        s3 = boto3.client('s3')
        print(f"🔍 Checking bucket: {BUCKET_NAME}...")
        
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        
        if 'Contents' in response:
            print(f"✅ Success! Found {len(response['Contents'])} files:")
            for obj in response['Contents']:
                print(f"  - {obj['Key']} ({obj['Size']} bytes)")
        else:
            print("❓ The bucket is empty. Did the pipeline finish running?")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify_s3_content()
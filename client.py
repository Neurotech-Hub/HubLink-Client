import requests
import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
import subprocess
import shutil

# Load environment variables from .env file
load_dotenv()

# Retrieve SECRET_URL from environment variables
SECRET_URL = os.getenv("SECRET_URL")

# Set local directory for syncing
LOCAL_DIRECTORY = "./data"

def get_s3_credentials(url):
    try:
        response = requests.get(url + ".json")
        response.raise_for_status()
        data = response.json()
        aws_access_key_id = data["aws_access_key_id"]
        aws_secret_access_key = data["aws_secret_access_key"]
        bucket_name = data["bucket_name"]
        return aws_access_key_id, aws_secret_access_key, bucket_name
    except requests.RequestException as e:
        print(f"Error fetching credentials: {e}")
        return None, None, None

def calculate_sync_requirements(aws_access_key_id, aws_secret_access_key, bucket_name, local_directory=LOCAL_DIRECTORY):
    if not aws_access_key_id or not aws_secret_access_key or not bucket_name:
        print("Invalid credentials. Unable to proceed.")
        return [], 0

    try:
        # Initialize S3 client
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        
        # Get the list of objects in the bucket
        response = s3.list_objects_v2(Bucket=bucket_name)
        
        files_to_sync = []
        total_size = 0
        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                local_file_path = os.path.join(local_directory, key)
                # Check if the file exists locally and if it matches the size of the S3 object
                if not os.path.exists(local_file_path) or os.path.getsize(local_file_path) != obj['Size']:
                    files_to_sync.append(key)
                    total_size += obj['Size']
            
            # Print the list of files that need syncing and the total size
            if files_to_sync:
                print("Files that need syncing:")
                for file in files_to_sync:
                    print(file)
                print(f"Total size required for sync: {total_size / (1024 * 1024):.2f} MB")
            else:
                print("All files are up to date.")
        else:
            print("No objects found in the bucket.")
        
        return files_to_sync, total_size
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Credential error: {e}")
    except ClientError as e:
        print(f"AWS Client error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return [], 0

def sync_s3_to_local_with_cli(bucket_name, aws_access_key_id, aws_secret_access_key, local_directory=LOCAL_DIRECTORY):
    try:
        # Check if AWS CLI is installed
        if not shutil.which("aws"):
            raise FileNotFoundError("AWS CLI not found. Please install AWS CLI to use the sync feature.")
        
        # Use AWS CLI to sync S3 bucket with local directory
        os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_id
        os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
        sync_command = [
            "aws", "s3", "sync", f"s3://{bucket_name}", local_directory
        ]
        subprocess.run(sync_command, check=True)
        print("Sync completed successfully.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Error during sync: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during sync: {e}")

def main():
    # Get S3 credentials
    aws_access_key_id, aws_secret_access_key, bucket_name = get_s3_credentials(SECRET_URL)
    
    # Calculate the files that need syncing and the required storage
    files_to_sync, total_size = calculate_sync_requirements(aws_access_key_id, aws_secret_access_key, bucket_name)
    
    # Ask for user confirmation before proceeding with sync
    if files_to_sync:
        user_input = input(f"{len(files_to_sync)} files need to be synced, totaling {total_size / (1024 * 1024):.2f} MB. Proceed? [Y/n]: ")
        if user_input.lower() not in ['', 'y', 'yes']:
            print("Sync aborted by user.")
            return
    
    # Sync S3 bucket with local directory using AWS CLI
    sync_s3_to_local_with_cli(bucket_name, aws_access_key_id, aws_secret_access_key)

if __name__ == "__main__":
    main()

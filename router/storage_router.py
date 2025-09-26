from fastapi import APIRouter, UploadFile, File, HTTPException
from google.cloud import storage
from uuid import uuid4
import os
from dotenv import load_dotenv
load_dotenv(override=False)

storage_api = APIRouter(prefix="/api/storage", tags=["storage-router"])

# Set your GCP bucket name and path to credentials
BUCKET_NAME = os.getenv("BUCKET_NAME")
CREDENTIALS_PATH = "gcp_key.json"

# Set GCP credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

@storage_api.post("/uploadImage")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed.")

    try:
        filename = f"image/{uuid4().hex}_{file.filename}"

        # Initialize GCS client and bucket
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)

        # Upload the file content
        blob.upload_from_file(file.file, content_type=file.content_type)

        # With Uniform Bucket-Level Access, making the *bucket* publicly readable
        # is sufficient. You don't need to call blob.make_public().
        # The public URL is directly constructible.
        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"
        return {"url": public_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@storage_api.put("/updateImage/{blob_name:path}")
async def update_image(blob_name: str, file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed.")

    try:
        # Initialize GCS client and bucket
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)

        if not blob.exists():
            raise HTTPException(status_code=404, detail=f"Image '{blob_name}' not found.")

        blob.upload_from_file(file.file, content_type=file.content_type)

        # The public URL remains the same if the blob name doesn't change
        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{blob_name}"
        return {"url": public_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@storage_api.get("/publicUrl/{blob_name:path}")
async def get_public_url(blob_name: str):
    try:
        # Initialize GCS client and bucket
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)

        if not blob.exists():
            raise HTTPException(status_code=404, detail=f"Image '{blob_name}' not found.")

        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{blob_name}"
        return {"url": public_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
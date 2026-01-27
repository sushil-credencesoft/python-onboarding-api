import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from router.onboard import onboard
from router.storage_router import storage_api
from function.credential_builder import create_credentials_file
from router.email_router import email_router



# Create credentials file and set environment variable
create_credentials_file()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

app = FastAPI(
    title="Automation Onboarding API",
    description="This App Used For Onboarding",
    version="1.0.0"
)

# ✅ CORS Configuration for specific domains and their subdomains
origins = [
    # Main domains
    "https://bookone.io",
    "https://thehotelmate.co",
    "https://thehotelmate.in",
    "https://thm-onboarding.bookone.io",
    "https://uat.onboard.bookone.io",
    "https://onboarding.bookonepms.com",
    
    # HTTP versions (if needed for development)
    "http://bookone.io",
    "http://thehotelmate.co",
    "http://thehotelmate.in",
    "http://api.thehotelmate.co",
    
    # Add specific subdomains if you know them
    # "https://api.bookone.io",
    # "https://admin.thehotelmate.co",
    
    # Development (remove in production)
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Your specific domains
    allow_credentials=True,         # Now you can use cookies/auth
    allow_methods=["*"],            # Allow all HTTP methods
    allow_headers=["*"],            # Allow all headers
    expose_headers=["*"],           # Explicitly expose all headers
)

# Include routers AFTER middleware
app.include_router(onboard)
app.include_router(storage_api)
app.include_router(email_router)

# Pydantic model for validation
class Item(BaseModel):
    name: str = Field(..., example="Apple")
    price: float = Field(..., gt=0, example=1.99)
    description: Optional[str] = Field(None, example="A fresh apple")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.post("/items/")
def create_item(item: Item):
    return {
        "message": "Item received",
        "item": item.model_dump()
    }

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Incoming request: {request.method} {request.url}")
    print(f"Origin: {request.headers.get('origin')}")
    response = await call_next(request)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
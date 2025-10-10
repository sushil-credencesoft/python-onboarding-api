import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from router.onboard import onboard
from router.storage_router import storage_api
from function.credential_builder import create_credentials_file


# Create credentials file and set environment variable
create_credentials_file()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

app = FastAPI(
    title="Automation Onboarding API",
    description="This App Used For Onboarding",
    version="1.0.0"
)

# ✅ Fix CORS: allow all origins properly
# If you truly want to expose API to all (no auth cookies etc.),
# disable allow_credentials or dynamically set origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Allow all origins
    allow_credentials=False,        # Must be False when "*" is used
    allow_methods=["*"],            # Allow all HTTP methods
    allow_headers=["*"],            # Allow all headers
    expose_headers=["*"],           # Explicitly expose all headers
)

# Include routers
app.include_router(onboard)
app.include_router(storage_api)

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
    response = await call_next(request)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

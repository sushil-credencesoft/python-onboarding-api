import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from router.onboard import onboard
from router.storage_router import storage_api
from function.credential_builder import create_credentials_file


create_credentials_file()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"


app = FastAPI(
    title="Automation Onboarding API",
    description="This App Used For Onboarding",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(onboard)
app.include_router(storage_api)

# Pydantic model for request validation
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
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)



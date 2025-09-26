from pydantic import BaseModel, EmailStr, Field, RootModel
from typing import Optional, Dict, List


# Fix: Use RootModel for roomPlan
class RoomPlan(RootModel[Dict[str, str]]):
    pass


# Fix: Use RoomPlan as a normal field
class RoomTypeDetail(BaseModel):
    roomStandardPrice: str
    roomPlan: RoomPlan


# Fix: This field has an alias due to space in "room numbers"
class FloorRoomDetails(BaseModel):
    room_numbers: List[int] = Field(..., alias="room numbers")


# Fix: Use RootModel for roomDetails
class RoomDetails(RootModel[Dict[str, Dict[str, FloorRoomDetails]]]):
    pass


class OnboardingData(BaseModel):
    BusinessName: str
    adminFirstName: str
    adminLastName: str
    address: Optional[str] = ""
    city: str
    country: str
    locality: str
    postcode: str
    state: str
    streetName: str
    streetNumber: str
    subUrb: str
    BusinessType: str
    email: EmailStr
    facebook: Optional[str] = ""
    fileName: Optional[str] = ""
    instagram: Optional[str] = ""
    twitter: Optional[str] = ""
    managerContactNo: str
    managerEmailAddress: Optional[str] = ""
    managerFirstName: str
    managerLastName: str
    mobile: str
    source: Optional[str] = ""
    status: Optional[str] = ""
    website: Optional[str] = ""
    gstNumber: Optional[str] = ""
    Longitude: Optional[str] = ""
    Latitude: Optional[str] = ""
    googlePlaceId: Optional[str] = ""
    bankName: Optional[str] = ""
    branchName: Optional[str] = ""
    accountName: Optional[str] = ""
    accountNumber: Optional[str] = ""
    swiftCode: Optional[str] = ""
    extraPersonCharge: int
    roomType: Dict[str, RoomTypeDetail]
    roomDetails: RoomDetails

    class Config:
        populate_by_name = True

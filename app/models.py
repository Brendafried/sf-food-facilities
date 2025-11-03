from pydantic import BaseModel
from typing import Optional

class FoodTruck(BaseModel):
    locationid: str
    applicant: str
    status: str

    # extra fields from the dataset
    facilitytype: Optional[str] = None
    locationdescription: Optional[str] = None
    address: Optional[str] = None
    blocklot: Optional[str] = None
    block: Optional[str] = None
    lot: Optional[str] = None
    permit: Optional[str] = None
    fooditems: Optional[str] = None

    # coordinates
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    x: Optional[float] = None   
    y: Optional[float] = None  

class NearbyFoodTruck(BaseModel):
    distance_m: float
    truck: FoodTruck

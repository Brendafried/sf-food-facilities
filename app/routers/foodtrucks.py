from fastapi import APIRouter, Request, Query
from typing import List, Optional
from app.models import FoodTruck, NearbyFoodTruck
from app.services.foodtrucks_service import filter_trucks, nearest_trucks

router = APIRouter()

def get_data(request: Request) -> List[FoodTruck]:
    return request.app.state.food_trucks

@router.get("/foodtrucks", response_model=List[FoodTruck])
def list_foodtrucks(
    request: Request,
    applicant: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    street: Optional[str] = Query(None),
    fooditem: Optional[str] = Query(None),
):
    data = get_data(request)
    return filter_trucks(
        data,
        applicant=applicant,
        status=status,
        street=street,
        fooditem=fooditem,
    )

@router.get("/foodtrucks/nearby", response_model=List[NearbyFoodTruck])
def list_nearby_foodtrucks(
    request: Request,
    lat: float = Query(...),
    lng: float = Query(...),
    status: Optional[str] = Query("APPROVED"),
    limit: int = Query(5, gt=0),
    fooditem: Optional[str] = Query(None, description="substring to match in fooditems, e.g. 'taco'"),
):
    data = get_data(request)
    return nearest_trucks(
        data,
        lat=lat,
        lng=lng,
        status=status,
        limit=limit,
        fooditem=fooditem,
    )

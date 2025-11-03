from typing import List, Optional
from app.models import FoodTruck
import math

def filter_trucks(
    trucks: List[FoodTruck],
    applicant: Optional[str] = None,
    status: Optional[str] = None,
    street: Optional[str] = None,
    fooditem: Optional[str] = None,
) -> List[FoodTruck]:
    result = trucks
    if applicant:
        a = applicant.lower()
        result = [t for t in result if a in t.applicant.lower()]
    if status:
        s = status.upper()
        result = [t for t in result if t.status.upper() == s]
    if street:
        st = street.lower()
        result = [t for t in result if t.address and st in t.address.lower()]
    if fooditem:
        fi = fooditem.lower()
        result = [t for t in result if t.fooditems and fi in t.fooditems.lower()]
    return result


def _simple_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Very simple distance just for sorting nearby trucks.
    """
    dlat = lat1 - lat2
    # adjust lon by latitude so east/west isn't too skewed
    dlon = (lon1 - lon2) * math.cos(math.radians(lat1))
    return dlat * dlat + dlon * dlon  # no sqrt needed for sorting


def nearest_trucks(
    trucks: List[FoodTruck],
    lat: float,
    lng: float,
    status: Optional[str] = "APPROVED",
    limit: int = 5,
    fooditem: Optional[str] = None,
):
    # filter by status
    if status and status.upper() != "ALL":
        trucks = [t for t in trucks if t.status.upper() == status.upper()]

    # filter by food item
    if fooditem:
        f = fooditem.lower()
        trucks = [t for t in trucks if t.fooditems and f in t.fooditems.lower()]

    scored = []
    for t in trucks:
        if t.latitude is None or t.longitude is None:
            continue
        dist = _simple_distance(lat, lng, t.latitude, t.longitude)
        scored.append((dist, t))

    scored.sort(key=lambda x: x[0])
    scored = scored[:limit]

    return [
        {
            "distance_m": d,
            "truck": t
        }
        for d, t in scored
    ]

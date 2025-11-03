import logging
import os
import requests
from app.models import FoodTruck

DEFAULT_URL = "https://data.sfgov.org/resource/rqzj-sfat.json"

logger = logging.getLogger(__name__)

def load_food_trucks():
    url = os.getenv("SF_FOOD_URL", DEFAULT_URL)

    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        rows = resp.json()
    except Exception as e:
        logger.error(f"Could not load SF food truck data from {url}: {e}")
        return []

    trucks = []
    for item in rows:
        latitude = _to_float(item.get("latitude"))
        longitude = _to_float(item.get("longitude"))
        x = _to_float(item.get("x"))
        y = _to_float(item.get("y"))

        trucks.append(
            FoodTruck(
                locationid=str(item.get("locationid", "")),
                applicant=item.get("applicant", "") or "",
                status=item.get("status", "") or "",
                facilitytype=item.get("facilitytype"),
                locationdescription=item.get("locationdescription"),
                address=item.get("address"),
                blocklot=item.get("blocklot"),
                block=item.get("block"),
                lot=item.get("lot"),
                permit=item.get("permit"),
                fooditems=item.get("fooditems"),
                latitude=latitude,
                longitude=longitude,
                x=x,
                y=y,
            )
        )
    return trucks

def _to_float(val):
    if val is None or val == "":
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None

from app.models import FoodTruck
from app.services.foodtrucks_service import (
    filter_trucks,
    nearest_trucks,
)


SAMPLE = [
    FoodTruck(
        locationid="1",
        applicant="TOASTY TRUCK",
        status="APPROVED",
        address="100 SANSOME ST",
        latitude=37.7901,
        longitude=-122.4013,
        fooditems="Tacos, Burritos",
    ),
    FoodTruck(
        locationid="2",
        applicant="COFFEE CART",
        status="EXPIRED",
        address="200 MARKET ST",
        latitude=37.7800,
        longitude=-122.4000,
        fooditems="Coffee, Donuts",
    ),
]


def test_filter_by_applicant():
    res = filter_trucks(SAMPLE, applicant="toast")
    assert len(res) == 1
    assert res[0].applicant == "TOASTY TRUCK"


def test_filter_by_street_partial():
    res = filter_trucks(SAMPLE, street="SANS")
    assert len(res) == 1
    assert res[0].address == "100 SANSOME ST"


def test_filter_by_status():
    res = filter_trucks(SAMPLE, status="APPROVED")
    assert len(res) == 1
    assert res[0].status == "APPROVED"


def test_nearest_defaults_to_approved():
    res = nearest_trucks(SAMPLE, 37.7901, -122.4013)
    # default should only include APPROVED
    assert len(res) == 1
    assert res[0]["truck"].locationid == "1"


def test_nearest_can_search_all_statuses():
    res = nearest_trucks(SAMPLE, 37.7901, -122.4013, status="ALL", limit=5)
    assert len(res) == 2

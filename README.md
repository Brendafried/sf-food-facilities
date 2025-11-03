# SF Mobile Food Facilities API

This is a backend-focused implementation of the “Food Facilities Challenge” using **FastAPI**.  
It exposes endpoints to:

- search food trucks by applicant name (with optional filter on `status`)
- search food trucks by (partial) street/address
- find the 5 nearest food trucks to a given latitude/longitude, defaulting to `APPROVED` but allowing other statuses
- (nice-to-have) filter nearby by a substring in `fooditems` (e.g. `taco`)

Data is loaded at startup from the public SODA endpoint:

- https://data.sfgov.org/resource/rqzj-sfat.json

---

## 1. Description of the problem and solution

**Problem:**  
Given the SF “Mobile Food Facility Permit” dataset, build an API that lets users search mobile food facilities by name and street, and find the nearest facilities to a location, with a focus on `status = APPROVED`. Include automated tests.

**Solution:**  
This app is a small FastAPI service that:

1. On startup, fetches the dataset from the SFGov SODA API and keeps it in memory.
2. Exposes REST endpoints under `/api`:
   - `GET /api/foodtrucks`  
     - filters by `applicant`, `status`, `street`, and optionally `fooditem`
   - `GET /api/foodtrucks/nearby`  
     - takes `lat` and `lng`
     - returns up to 5 closest trucks
     - defaults to `APPROVED` but can be overridden with `status=ALL`
     - can optionally filter by `fooditem`
3. Includes pytest tests for both the service logic (filtering, nearby) and the API.
4. Includes a Dockerfile, docker-compose, and a Makefile to run the app and tests easily.
5. Uses FastAPI’s built-in OpenAPI/Swagger UI at `/docs` to quickly test endpoints.

---

## 2. Reasoning behind technical / architectural decisions

- **FastAPI**: lightweight, fast to build, automatically generates API docs (`/docs`), easy to test with `TestClient`. This also satisfies the “Use an API documentation tool” bonus.
- **In-memory data**: for a coding challenge, loading from the public endpoint at startup is simpler than setting up a database. It makes the app self-contained.
- **Simple distance calculation**: since all points are in San Francisco, a simple planar distance (adjusted by latitude) is “good enough” to rank nearby trucks. In a real system, we’d use proper geospatial distance or an external matrix API.
- **Separation into `routers/`, `services/`, and `models.py`**: keeps request/response models, business logic, and FastAPI routing separate and testable.
- **Docker**: Allows for running the exact same environment.
- **Makefile**: small improvement so common commands are one-liners.

---

## 3. Critique

### If I had more time, I would…
- Persist the data in a real database (Postgres with PostGIS) and query the nearest trucks using spatial indexes.
- Add pagination and sorting to `GET /api/foodtrucks`.
- Add validation around lat/lng ranges and better error responses.
- Add a small frontend to visualize nearby trucks on a map.
- Add CI to run `pytest` on every push.

### Trade-offs I made
- **In-memory storage**: super simple, but every app restart re-downloads data, and it won’t scale to very large datasets.
- **Simple distance** instead of Haversine / Google / OSRM: faster to read and implement, but not road or traffic-aware. For a demo and a small geographic area, I thought this would be acceptable.
- **No auth / rate limiting**: fine for a test project, but not for public deployment.
- **Single dataset source**: if the SFGov endpoint is down or rate-limited, we return an empty list. In production we’d cache to disk or a DB.

### Things I left out
- Persistent storage (DB)
- Background jobs to refresh the dataset on a schedule
- Proper logging/metrics
- Validation of `status` against a fixed enum
- Real geospatial queries

### Scaling concerns & how to solve them
- **Problem:** downloading the dataset on every startup is slow and fragile.  
  **Solution:** cache the JSON to disk / S3 / DB and refresh periodically.
- **Problem:** in-memory filtering is O(n) every request.  
  **Solution:** move to a DB and add indexes on `applicant`, `status`, and address; for geospatial use PostGIS (`ORDER BY <-> LIMIT 5`).
- **Problem:** single-process FastAPI won’t handle lots of traffic.  
  **Solution:** run behind a reverse proxy (nginx) and scale replicas (uvicorn/gunicorn workers) with Docker/K8s.
- **Problem:** geospatial accuracy.  
  **Solution:** use a proper distance function (Haversine) or a routing API like Google Distance Matrix.

---

## 4. How to run

### Prereqs
- Python 3.11+ (I used 3.12)
- Or Docker

### Option A: run locally

1. Create and activate env (conda or venv)
   ```bash
   pip install -r requirements.txt
   ```
2. Run
   ```bash 
   make dev
   ```
3. Open
  - Swagger UI: http://127.0.0.1:8002/docs
  - Health: http://127.0.0.1:8002/health

### Option B: with Docker

1. Run 
   ```bash
    make dc-up
   ```
2. Open
  - Swagger UI: http://127.0.0.1:8002/docs
  - Health: http://127.0.0.1:8002/health

## 5. How to run tests

Tests live under tests/ and use pytest plus FastAPI’s TestClient.

Run locally:
```bash 
  pytest 
  ```

Run in Docker (after building image):
```bash 
  docker run --rm sf-food-api pytest
  ```

That shows the API starts and the core filters (applicant, street, status, nearby) behave the way the challenge described.

## 6. Endpoints

`GET /health`
Returns a simple JSON payload to show the service is up.

`GET /api/foodtrucks`
Query params:

- applicant: substring, case-insensitive

- status: exact match, e.g. APPROVED

- street: substring on the address, so SAN matches SANSOME ST

- fooditem: substring on the FoodItems field from the dataset
Returns a list of trucks with the fields from the dataset (applicant, status, address, fooditems, etc.).

`GET /api/foodtrucks/nearby`
Query params:

- lat (required)

- lng (required)

- status (optional, default APPROVED; if you pass status=ALL it will include any status)

- limit (optional, default 5)

- fooditem (optional)
Returns the closest trucks to the given point, up to the limit. The distance field in the response is the value used for sorting, not real meters, which is fine for SF and for this challenge.


If there are any questions about the work for this project please reach out to me
Brenda Halpern
friedbrenda@gmail.com

# Voice Agent Dillon

A web application for automating insurance verification calls using AI voice agents. Now available in both Flask and FastAPI versions!

## Features

- Create automated calls to insurance providers
- Track call history and status
- View detailed call results and structured data
- RESTful API for integration with other systems
- FastAPI version with improved performance and automatic API documentation

## Setup and Installation

### Flask Version (Original)

1. Install the required dependencies:

   ```
   pip install flask vapi
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

### FastAPI Version

1. Install the required dependencies:

   ```
   pip install fastapi uvicorn[standard] python-multipart jinja2 vapi
   ```

2. Run the application:

   ```
   python run_fastapi.py
   ```

   Or directly with uvicorn:

   ```
   uvicorn app_fastapi:app --reload
   ```

3. Open your web browser and navigate to:
   ```
   http://127.0.0.1:8000/
   ```
4. API Documentation (automatically generated):
   ```
   http://127.0.0.1:8000/docs  # Swagger UI
   http://127.0.0.1:8000/redoc # ReDoc
   ```

## API Documentation

> Note: With the FastAPI version, you can also view interactive API documentation at `/docs` or `/redoc` endpoints.

### 1. Create a New Call

Initiates a new automated call to the specified phone number.

**Endpoint:** `POST /api/calls`

**Request Body:**

```json
{
  "phone_number": "+1234567890"
}
```

**Response:**

```json
{
  "success": true,
  "call_id": "abc123def456"
}
```

### 2. Get Call Results

Retrieves the details and results of a specific call.

**Endpoint:** `GET /api/calls/{call_id}`

**Response:**

```json
{
  "id": "abc123def456",
  "summary": "Call summary text",
  "structured_data": {
    "policy_active": true,
    "effective_date": "01-01-2025",
    "benefit_year_type": "calendar",
    "plan_type": "PPO",
    "in_network_status": "in-network",
    "out_of_pocket_max_individual": "$1000",
    "out_of_pocket_max_family": "$3000",
    "missing_tooth_clause": "not applicable",
    "downgrade_posterior_composite": false,
    "freq_fmx_pano": "once every 3 years",
    "replacement_clause_crown_bridge_implant": "5 years"
  },
  "ended_reason": "completed",
  "success_evaluation": true
}
```

### 3. List All Calls

Returns a list of all calls, sorted by date (newest first).

**Endpoint:** `GET /api/calls`

**Response:**

```json
[
  {
    "id": "abc123def456",
    "phone_number": "+1234567890",
    "timestamp": "2025-09-09 12:34:56",
    "status": "completed"
  },
  {
    "id": "def456ghi789",
    "phone_number": "+1987654321",
    "timestamp": "2025-09-08 10:11:12",
    "status": "initiated"
  }
]
```

## Web Interface

The application provides a user-friendly web interface with the following pages:

1. **Home Page** (`/`): Create new calls by entering a phone number
2. **Call History** (`/calls`): View all calls with their status
3. **Call Details** (`/calls/{call_id}`): View detailed results for a specific call

## Auto-Refresh Functionality

- In-progress calls are automatically refreshed every 10 seconds on the details page
- Call history list is refreshed every 30 seconds if there are any in-progress calls
- Both auto-refresh features can be toggled on/off by the user

## Data Storage

Call records are stored in memory during runtime and backed up to a JSON file (`call_records.json`) for persistence between application restarts.

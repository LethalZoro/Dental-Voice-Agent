from vapi import Vapi
from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import datetime
import json
import os
import uvicorn

# Load environment variables from .env file
load_dotenv()

# Create FastAPI app
app = FastAPI(title="Dental Voice Agent System")

# Create a custom Jinja2Templates class to handle url_for
class CustomJinja2Templates(Jinja2Templates):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env.globals["url_for"] = self.url_for
    
    def url_for(self, name, **path_params):
        # Handle "static" route specially
        if name == "static" and "filename" in path_params:
            return f"/static/{path_params['filename']}"
        return app.url_path_for(name, **path_params)

# Configure Jinja2 templates
templates = CustomJinja2Templates(directory="templates")

# Mount static files directory if it exists
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize the Vapi client using API key from environment variables
client = Vapi(token=os.getenv("VAPI_API_KEY"))

# Store call records (in-memory database for simplicity)
# In a production environment, use a proper database
call_records = []

# Create Pydantic models for request/response validation
class PhoneNumberRequest(BaseModel):
    phone_number: str

class CallResponse(BaseModel):
    success: bool
    call_id: str

class ErrorResponse(BaseModel):
    error: str

class CallData(BaseModel):
    id: str
    status: str
    summary: Optional[str] = None
    structured_data: Dict[str, Any] = {}
    ended_reason: Optional[str] = None
    success_evaluation: Optional[bool] = None
    started_at: Optional[datetime.datetime] = None
    ended_at: Optional[datetime.datetime] = None
    duration: Optional[str] = None
    transcript: Optional[str] = None
    recording_url: Optional[str] = None
    cost: Optional[float] = None
    started_at_formatted: Optional[str] = None
    ended_at_formatted: Optional[str] = None

patient_clinic_data = {
    "appointment_date": "01-07-2025",
    "insurance_rep": "WEB",
    "insurance_carrier": "METLIFE PPO",
    "insurance_phone": "(800)275-4638",
    
    "insured_name": "Jane, Patrick",
    "insured_dob": "09-07-1999",
    "insured_ss": "N/A",
    "insured_id": "104389769",

    "relationship_to_patient": "SELF",
    
    "patient_name": "Jane, Patrick",
    "patient_dob": "09-07-1999",
    "employer": "FEDERAL EMPLOYEES DENTAL AND",
    "group_number": "121332",

    "claims_address": "PO BOX 14093 EL PASO TX 79998",
    "payor_id": "65978",
    
    "clinic_name": "Blue Lines Dental Clinic",
    "practice_tax_id": "123456",
    "treating_dentist_name": "Dr. Mustafa",
    "dentist_npi": "789012",
}

def call_squad(phone_num):
    try:
        test_call = client.calls.create(
            name="test_call",
            squad={
                "members": [
                    {
                        "assistantId": "5cd5625c-2f48-46e1-9575-3dc2b5efedc4", # 1. Introduction
                        "assistantDestinations": [
                            {
                                "type": "assistant",
                                "assistantId": "7ca934ef-e8fa-4308-8b80-abdbba8d9e80",
                                "description": "Occurs once the payment_basis and in_network_status are captured.",
                            }
                        ],
                        
                        "assistantOverrides": {
                            "variableValues": patient_clinic_data
                        }
                    },
                    {
                        "assistantId": "7ca934ef-e8fa-4308-8b80-abdbba8d9e80", # 2. Deductibles & Maximums
                        "assistantDestinations": [
                            {
                                "type": "assistant",
                                "assistantId": "eff2f1a7-4614-43bc-96ab-cd53ffd44a72",
                                "description": "Occurs once the waiting_period and missing_tooth_clause are captured.",
                            }
                        ],
                        
                        "assistantOverrides": {
                            "variableValues": patient_clinic_data
                        }
                    },
                    {
                        "assistantId": "eff2f1a7-4614-43bc-96ab-cd53ffd44a72", # 3. Coinsurance Percentages
                        "assistantDestinations": [
                            {
                                "type": "assistant",
                                "assistantId": "9d6589f4-d0f3-4565-b2a9-7165dda1fae2",
                                "description": "Occurs once the coinsurance_periodontics and coinsurance_oral_surgery are All captured.",
                            }
                        ],
                        
                        "assistantOverrides": {
                            "variableValues": patient_clinic_data
                        }
                    },
                    {
                        "assistantId": "9d6589f4-d0f3-4565-b2a9-7165dda1fae2", # 4. Freq A
                        "assistantDestinations": [
                            {
                                "type": "assistant",
                                "assistantId": "2f460c63-bd99-4393-8c17-10b9864e9a14",
                                "description": "Occurs once the srp_4341_coverage and all_four_quads_same_day_allowed are captured.",
                            }
                        ],
                        
                        "assistantOverrides": {
                            "variableValues": patient_clinic_data
                        }
                    },
                    {
                        "assistantId": "2f460c63-bd99-4393-8c17-10b9864e9a14", # 5. Freq B
                        "assistantDestinations": [
                            {
                                "type": "assistant",
                                "assistantId": "f40c8e73-5c26-4e1e-8bd2-2fb04106f4cd",
                                "description": "Occurs once the perio_maint_4910_coverage and missing_tooth_clause_applies are captured.",
                            }
                        ],
                        
                        "assistantOverrides": {
                            "variableValues": patient_clinic_data
                        }
                    },
                    {
                        "assistantId": "f40c8e73-5c26-4e1e-8bd2-2fb04106f4cd", # 6. Freq C
                        "assistantDestinations": [
                            {
                                "type": "assistant",
                                "assistantId": "98b18cf5-3975-4352-9c4c-2c634b3f6108",
                                "description": "Occurs once the ortho_balance_payment_schedule and ortho_work_in_progress_applies and occlusal_guard_9944_covered are All captured.",
                            }
                        ],
                        
                        "assistantOverrides": {
                            "variableValues": patient_clinic_data
                        }
                    },
                ]
            },
            phone_number_id=os.getenv("PHONE_NUMBER_ID"),
            customer={
                "number": phone_num,  
            },
        )

        print(f"Test call initiated: {test_call.id}")
        
        # Store call record with patient and clinic data
        call_record = {
            "id": test_call.id,
            "phone_number": phone_num,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "scheduled",  # Initial status is scheduled
            "patient_data": patient_clinic_data.copy()  # Store a copy of the patient data used for this call
        }
        call_records.append(call_record)
        
        # Save to JSON file as backup
        save_call_records()
        
        return test_call.id
    except Exception as error:
        print(f"Error testing workflow: {error}")
        raise error

def get_call_results(call_id):
    try:
        call = client.calls.get(id=call_id)
        
        # Determine the call status based on different properties
        call_status = "scheduled"  # Default status
        
        if hasattr(call, 'started_at') and call.started_at:
            call_status = "in_progress"
            
        if hasattr(call, 'ended_reason'):
            if call.ended_reason == "completed":
                # Check if evaluation is available and use it for status
                if (hasattr(call, 'analysis') and 
                    hasattr(call.analysis, 'success_evaluation') and 
                    call.analysis.success_evaluation is not None):
                    # Convert string "true"/"false" to boolean values
                    success_eval = False
                    if isinstance(call.analysis.success_evaluation, str):
                        success_eval = call.analysis.success_evaluation.lower() == "true"
                    else:
                        success_eval = bool(call.analysis.success_evaluation)
                    call_status = "completed" if success_eval else "failed"
                else:
                    call_status = "completed"
            elif call.ended_reason:
                call_status = call.ended_reason
        
        # Get analysis data with proper null checks
        analysis_data = {
            "id": call_id,
            "status": call_status,
            "summary": None,
            "structured_data": {},
            "ended_reason": call.ended_reason if hasattr(call, 'ended_reason') else None,
            "success_evaluation": None,
            "started_at": call.started_at if hasattr(call, 'started_at') else None,
            "ended_at": call.ended_at if hasattr(call, 'ended_at') else None,
            "duration": None,  # Will calculate if both timestamps exist
            "transcript": call.transcript if hasattr(call, 'transcript') else None,
            "recording_url": call.recordingUrl if hasattr(call, 'recordingUrl') else None,
            "cost": call.cost if hasattr(call, 'cost') else None
        }
        
        # Extract analysis data carefully
        if hasattr(call, 'analysis'):
            if hasattr(call.analysis, 'summary'):
                analysis_data["summary"] = call.analysis.summary
                
            if hasattr(call.analysis, 'structured_data'):
                analysis_data["structured_data"] = call.analysis.structured_data
                
            if hasattr(call.analysis, 'success_evaluation'):
                # Convert string "true"/"false" to boolean values
                if isinstance(call.analysis.success_evaluation, str):
                    analysis_data["success_evaluation"] = call.analysis.success_evaluation.lower() == "true"
                else:
                    analysis_data["success_evaluation"] = bool(call.analysis.success_evaluation)
                    
        # Calculate call duration if we have both timestamps
        if analysis_data["started_at"] and analysis_data["ended_at"]:
            try:
                # Handle datetime objects directly
                start_time = analysis_data["started_at"]
                end_time = analysis_data["ended_at"]
                
                # Calculate duration in seconds
                duration_seconds = (end_time - start_time).total_seconds()
                
                # Format as minutes and seconds
                minutes = int(duration_seconds // 60)
                seconds = int(duration_seconds % 60)
                analysis_data["duration"] = f"{minutes}m {seconds}s"
                
                # Format timestamps for display
                analysis_data["started_at_formatted"] = start_time.strftime("%Y-%m-%d %H:%M:%S UTC")
                analysis_data["ended_at_formatted"] = end_time.strftime("%Y-%m-%d %H:%M:%S UTC")
            except Exception as e:
                print(f"Error calculating duration: {e}")
                # Provide a fallback
                analysis_data["duration"] = "Unknown"
        
        # Update call record
        updated = False
        for call_record in call_records:
            if call_record["id"] == call_id:
                call_record["status"] = call_status
                call_record["results"] = analysis_data
                updated = True
                break
                
        # If no record found, create one
        if not updated:
            call_record = {
                "id": call_id,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": call_status,
                "results": analysis_data
            }
            
            # Get phone number if available
            if hasattr(call, 'customer') and hasattr(call.customer, 'number'):
                call_record["phone_number"] = call.customer.number
                
            call_records.append(call_record)
                
        # Save to JSON file as backup
        save_call_records()
        
        return analysis_data
    except Exception as error:
        print(f"Error retrieving call results: {error}")
        raise error

def save_call_records():
    """Save call records to a JSON file in /tmp directory"""
    # Create /tmp directory if it doesn't exist
    if not os.path.exists('/tmp'):
        try:
            os.makedirs('/tmp', exist_ok=True)
            print("Created /tmp directory")
        except Exception as e:
            print(f"Could not create /tmp directory: {e}")
    
    # Use /tmp directory on Vercel or local directory in development
    file_path = '/tmp/call_records.json' if os.path.exists('/tmp') else 'call_records.json'
    
    # Ensure the directory for the file exists
    os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)
    
    try:
        with open(file_path, 'w') as f:
            json.dump(call_records, f, indent=4, default=str)
        print(f"Saved call records to {file_path}")
    except Exception as e:
        print(f"Error saving call records to {file_path}: {e}")

def load_call_records():
    """Load call records from JSON file if it exists"""
    global call_records
    
    # Create /tmp directory if it doesn't exist
    if not os.path.exists('/tmp'):
        try:
            os.makedirs('/tmp', exist_ok=True)
            print("Created /tmp directory")
        except Exception as e:
            print(f"Could not create /tmp directory: {e}")
    
    # Try /tmp directory first (for Vercel), then local directory
    file_paths = ['/tmp/call_records.json', 'call_records.json']
    
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    call_records = json.load(f)
                    print(f"Loaded call records from {file_path}")
                    return
        except Exception as e:
            print(f"Error loading call records from {file_path}: {e}")
    
    print("No call records found or could be loaded")

# Application startup event
@app.on_event("startup")
async def startup_event():
    # Create /tmp directory if it doesn't exist (useful for Vercel)
    if not os.path.exists('/tmp'):
        try:
            os.makedirs('/tmp', exist_ok=True)
            print("Created /tmp directory during startup")
        except Exception as e:
            print(f"Could not create /tmp directory during startup: {e}")
    
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    # Create static directory and js subdirectory if they don't exist
    os.makedirs('static/js', exist_ok=True)
    # Initialize call records from file on startup
    load_call_records()

# API Routes
@app.post("/api/calls", response_model=CallResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def create_call(request: PhoneNumberRequest):
    if not request.phone_number:
        raise HTTPException(status_code=400, detail="Phone number is required")
    
    try:
        call_id = call_squad(request.phone_number)
        return {"success": True, "call_id": call_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/calls/{call_id}", response_model=Dict[str, Any], responses={500: {"model": ErrorResponse}})
async def get_call(call_id: str):
    try:
        call_data = get_call_results(call_id)
        return call_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/calls", response_model=List[Dict[str, Any]])
async def get_all_calls():
    return sorted(call_records, key=lambda x: x.get("timestamp", ""), reverse=True)

# Web Routes
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/calls")
async def calls_page(request: Request):
    sorted_calls = sorted(call_records, key=lambda x: x.get("timestamp", ""), reverse=True)
    return templates.TemplateResponse("calls.html", {"request": request, "calls": sorted_calls})

@app.get("/calls/{call_id}")
async def call_details(request: Request, call_id: str):
    # Always fetch the latest data from the API for the call details page
    try:
        call_data = get_call_results(call_id)
        
        # Find the call record
        found_call = None
        for call in call_records:
            if call["id"] == call_id:
                found_call = call
                break
        
        # If call wasn't found in records, create a new record
        if not found_call:
            new_call = {
                "id": call_id,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": call_data.get("status", "unknown"),
                "results": call_data
            }
            call_records.append(new_call)
            save_call_records()
            found_call = new_call
            
        return templates.TemplateResponse("call_details.html", {"request": request, "call": found_call})
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

@app.post("/create_call")
async def create_call_web(
    request: Request,
    phone_number: str = Form(...),
    appointment_date: str = Form(...),
    insurance_rep: str = Form(...),
    insurance_carrier: str = Form(...),
    insurance_phone: str = Form(...),
    insured_name: str = Form(...),
    insured_dob: str = Form(...),
    insured_ss: str = Form(...),
    insured_id: str = Form(...),
    relationship_to_patient: str = Form(...),
    patient_name: str = Form(...),
    patient_dob: str = Form(...),
    employer: str = Form(...),
    group_number: str = Form(...),
    claims_address: str = Form(...),
    payor_id: str = Form(...),
    clinic_name: str = Form(...),
    practice_tax_id: str = Form(...),
    treating_dentist_name: str = Form(...),
    dentist_npi: str = Form(...)
):
    # Create form data dictionary
    form_data = {
        "appointment_date": appointment_date,
        "insurance_rep": insurance_rep,
        "insurance_carrier": insurance_carrier,
        "insurance_phone": insurance_phone,
        "insured_name": insured_name,
        "insured_dob": insured_dob,
        "insured_ss": insured_ss,
        "insured_id": insured_id,
        "relationship_to_patient": relationship_to_patient,
        "patient_name": patient_name,
        "patient_dob": patient_dob,
        "employer": employer,
        "group_number": group_number,
        "claims_address": claims_address,
        "payor_id": payor_id,
        "clinic_name": clinic_name,
        "practice_tax_id": practice_tax_id,
        "treating_dentist_name": treating_dentist_name,
        "dentist_npi": dentist_npi
    }
    
    try:
        # Update global patient_clinic_data with form values
        global patient_clinic_data
        patient_clinic_data = form_data
        
        call_id = call_squad(phone_number)
        return RedirectResponse(url=f"/calls/{call_id}", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "error": str(e)})

if __name__ == "__main__":
    # Run the FastAPI app with uvicorn
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=debug)

# For Vercel serverless deployment
app_handler = app
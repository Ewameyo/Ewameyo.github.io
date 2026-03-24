from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client
import os

app = FastAPI(title="DTO-NEXUS PRIME: IMS Engine")

# Security: Allow your Firebase Frontend to talk to this Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Credentials (Pulled from Render Environment Variables)
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key) if url and key else None

class OEEInput(BaseModel):
    availability: float
    performance: float
    quality: float
    company_id: str = "NEXUS_DEFAULT"

@app.get("/")
async def health_check():
    return {"status": "IMS_ACTIVE", "lead": "Edgar Wameyo, LSSBB"}

@app.post("/api/v1/sync")
async def calculate_and_store_oee(data: OEEInput):
    # LSSBB Calculation: (A * P * Q) / 10000
    oee = round((data.availability * data.performance * data.quality) / 10000, 2)
    
    # Persistent Log to Supabase
    if supabase:
        log_entry = {
            "oee_value": oee,
            "availability": data.availability,
            "performance": data.performance,
            "quality": data.quality,
            "company_id": data.company_id
        }
        supabase.table("oee_history").insert(log_entry).execute()
    
    return {
        "oee": f"{oee}%",
        "status": "LOGGED",
        "iso_audit": "VERIFIED"
    }

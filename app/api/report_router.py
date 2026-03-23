import traceback
from fastapi import APIRouter, HTTPException
from app.schemas.report import ReportResponse
from app.services import report_service 

router = APIRouter(tags=["Report"])

@router.get("/report/{org}", response_model=ReportResponse)
async def get_org_access_report(org: str, include_private: bool = False):
    try:
        # Generate the report
        return await report_service.generate_report(org, include_private)
    
    except Exception as e:
        # THIS WILL PRINT THE ACTUAL ERROR TO YOUR TERMINAL
        print("\n" + "="*50)
        print("🚨 BACKEND CRASH DETECTED")
        traceback.print_exc()
        print("="*50 + "\n")
        
        raise HTTPException(status_code=500, detail=str(e))
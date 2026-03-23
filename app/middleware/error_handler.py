from fastapi import Request
from fastapi.responses import JSONResponse
from app.schemas.error import ErrorResponse

async def global_exception_handler(request: Request, exc: Exception):
    """
    Catches any unhandled exceptions in the application and returns a structured JSON 
    response using the ErrorResponse schema, preventing the server from crashing.
    """
    error_msg = str(exc)
    print(f"ERROR:    Unhandled Exception: {error_msg}")
    
    # We serialize the Pydantic model to dict for the JSONResponse
    error_content = ErrorResponse(
        error="Internal Server Error",
        message="An unexpected error occurred while processing the request."
    ).model_dump()
    
    return JSONResponse(
        status_code=500,
        content=error_content
    )
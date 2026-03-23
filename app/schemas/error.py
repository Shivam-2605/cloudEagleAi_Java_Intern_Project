from pydantic import BaseModel

class ErrorResponse(BaseModel):
    """
    Standardized error response model for all API errors.
    """
    error: str
    message: str
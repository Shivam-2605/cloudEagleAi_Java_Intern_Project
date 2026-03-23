import time
from fastapi import Request

async def log_requests(request: Request, call_next):
    """
    Middleware that logs the HTTP method, path, response status, 
    and the time it took to process the request.
    """
    start_time = time.time()
    
    # Process the request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = (time.time() - start_time) * 1000
    
    # Log the result
    print(f"INFO:     [{request.method}] {request.url.path} - Status: {response.status_code} - {process_time:.2f}ms")
    
    return response
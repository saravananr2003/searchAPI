from fastapi import FastAPI, HTTPException
from .schemas import LookupRequest, LookupResponse
from .crud import get_id_by_fields
from .config import settings

app = FastAPI(title="Snowflake Lookup API")

@app.post("/lookup", response_model=LookupResponse)
def lookup(request: LookupRequest):
    try:
        id_value, found, detail = get_id_by_fields(request)
        return LookupResponse(id=id_value, found=found, detail=detail)
    except Exception as e:
        # log.error(...)  # in real app
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.api_host, port=settings.api_port, reload=True)

from pydantic import BaseModel

class LookupRequest(BaseModel):
    name: str
    address1: str
    address2: str | None = None
    city: str
    state: str
    zip: str
    phone: str

class LookupResponse(BaseModel):
    id: int | None
    found: bool
    detail: str

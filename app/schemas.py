from typing import Dict, List, Any

from pydantic import BaseModel


class AccountsRequest(BaseModel):
	AccountName: str
	AddressLine1: str  # Address line 1
	AddressLine2: str  # Address line 2
	CityName: str  # City Name
	StateCode: str  # State Code
	ZipCode: str  # Zip Code
	Zip4Code: str  # Zip Code
	CountryCode: str  # Country Code
	PhoneNumber: str  # Phone number


class AccountsResponse(BaseModel):
	site_info:Any
	found: bool
	detail: str


class ContactsRequest(BaseModel):
	Prefix: str
	FirstName: str
	MiddleInitial: str
	LastName: str
	Suffix: str
	address1: str  # Address line 1
	address2: str  # Address line 2
	city: str  # City Name
	state: str  # State Code
	zip: str  # Zip Code
	email: str  # Email address
	phone: str  # Phone number


class ContactsResponse(BaseModel):
	id: int
	found: bool
	detail: str

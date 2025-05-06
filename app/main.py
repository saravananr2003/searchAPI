from fastapi import FastAPI, HTTPException
from .schemas import AccountsRequest, AccountsResponse, ContactsRequest, ContactsResponse
from .crud import get_id_by_fields
from .config import settings

app = FastAPI(title="Snowflake Lookup API")


@app.post("/accountlookup", response_model=AccountsResponse)
def lookup(request: AccountsRequest):
	try:
		print (request)
		id_value, found, detail = get_id_by_fields(request)
		print("id_value")
		return AccountsResponse(site_info=id_value, found=found, detail=detail)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


# @app.post("/contactlookup", response_model=AccountsResponse)
# def lookup(request: ContactsRequest):
# 	try:
# 		id_value, found, detail = get_id_by_fields(request)
# 		# return ContactsResponse(id=id_value, found=found, detail=detail)
# 	except Exception as e:
# 		# log.error(...)  # in real app
# 		raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
	import uvicorn

	uvicorn.run("app.main:app", host=settings.api_host, port=settings.api_port, reload=True)

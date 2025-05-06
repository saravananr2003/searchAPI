import json
import uuid
from typing import Tuple

from . import schemas
from .database import get_connection
from .schemas import AccountsRequest


def get_org_id_from_tamr(request: AccountsRequest):
	import requests
	base_url = ("https://staples-prod-2.tamrfield.com/llm/api/v1/projects/2-B%20Site%20Mastering%20v2%3Amatch"
				"?type=clusters")
	headers = {
		"Content-Type": "application/json",
		"Accept": "application/json",
		"Authorization": "BasicCreds QlVfQVBQX1VTRVI6QlVfQVBQX1VTRVI="
	}

	payload = {
		"recordId": str(uuid.uuid4()),
		"record": {
			"site_address_1": [request.AddressLine1],
			"site_address_2": [request.AddressLine2],
			"site_address_full": [f"{request.AddressLine1} {request.AddressLine2}"],
			"site_city": [request.CityName],
			"site_country": [request.CountryCode],
			"site_zip5": [request.CityName],
			"site_zip9": [f"{request.ZipCode}-{request.Zip4Code}"],
			"site_phone_7": [request.PhoneNumber[:7]],
			"site_phone_areacode": [request.PhoneNumber[:3]],
			"site_state": [request.StateCode],
			"business_name": [request.AccountName],
			"site_zip4": [request.Zip4Code],
			"phone_number_most_frequent": [request.PhoneNumber],
			"site_phone_full_number": [request.PhoneNumber],
			"site_phone_number_10dig": [request.PhoneNumber],
			"COMPANY_NAME": [request.AccountName],
			"site_phone_6": [request.PhoneNumber[:6]],
			"ml_company_name": [request.AccountName.replace(' ', '')],
			"ml_company_first_word": [request.AccountName.split()[0]],
			"site_address_1_original": [request.AddressLine1],
			"business_name_gr": [request.AccountName]
		}
	}

	try:
		response = requests.post(base_url, headers=headers, json=payload, timeout=30)
		if response.status_code == 200:
			return [
				[item.get("clusterId"), item.get("avgMatchProb")]
				for item in (json.loads(line) for line in response.text.strip().splitlines() if line.strip())
			]
		print(f"Error: {response.status_code} - {response.text}")
	except requests.exceptions.RequestException as e:
		print(f"Request failed: {e}")
	return None


def get_id_by_fields(req: AccountsRequest) -> tuple[json, bool, str]:
	print("Request: ", req)
	org_id_list = get_org_id_from_tamr(req)
	# print("Org ID: {0}".format([item[0] for item in org_id_list]))
	# org_id_list = [['65ffff63-a48f-3eef-9d5c-f2d19504cc28', 0.6], ['63ca7b73-1a51-3fcb-8857-9b94d54f32f8', 0.8]]
	org_ids = "', '".join(item[0] for item in org_id_list)
	print (org_ids)
	ls_sql = (" SELECT site_id, source_type_code, "
			  "        listagg(source_id, '|' ) WITHIN GROUP ( ORDER BY row_update_timestamp DESC) source_id_list"
			  "   FROM customer.CURATED.SOURCE_TO_GOLDEN_XREF"
			  f" WHERE site_id in ('{org_ids}')"
			  "  GROUP BY ALL")

	conn = get_connection()
	try:
		with conn.cursor() as cur:
			cur.execute(ls_sql)
			rows = cur.fetchall()

		grouped_data = {}
		for site_id, source_type, source_id in rows:
			grouped_data.setdefault(site_id, {"site_id": site_id, "sources": []})["sources"].append(
				{"source_type": source_type, "source_id": source_id}
			)

		result_json = json.dumps(list(grouped_data.values()))
		return result_json, True, "Record found"
	except Exception as e:
		print(f"Error: {e}")
		return None, False, str(e)
	finally:
		conn.close()
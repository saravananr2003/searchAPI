import json
import uuid

from .database import get_connection
from .schemas import AccountsRequest

def call_tamr_api(AccountsRequest):
    import requests
    base_url = (
        "https://staples-prod-2.tamrfield.com/llm/api/v1/projects/2-B%20Site%20Mastering%20v2%3Amatch"
        "?type=clusters")

    headers = {"Content-Type": "application/json", "Accept": "application/json",
               "Authorization": "BasicCreds QlVfQVBQX1VTRVI6QlVfQVBQX1VTRVI="}
    ls_org_name = AccountsRequest.AccountName
    ls_addr1 = AccountsRequest.AddressLine1
    ls_addr2 = AccountsRequest.AddressLine2
    ls_city_name = AccountsRequest.CityName
    ls_state_cd = AccountsRequest.StateCode
    ls_zip_cd = AccountsRequest.ZipCode
    ls_zip4_cd = AccountsRequest.Zip4Code
    ls_country_cd = AccountsRequest.CountryCode
    ls_phone = AccountsRequest.PhoneNumber
    ls_ph_areacd = AccountsRequest.PhoneNumber[:3]
    ls_rec_id  = uuid.uuid4()

    # ls_rec_id = str(record['BU_REC_ID'])
    payload = {
        "recordId": f"{ls_rec_id}",
        "record": {
            "site_address_1": [f"{ls_addr1}"],
            "site_address_2": [f"{ls_addr2}"],
            "site_address_full": [f"{ls_addr1} {ls_addr2}"],
            "site_city": [f"{ls_city_name}"],
            "site_country": [f"{ls_country_cd}"],
            "site_zip5": [f"{ls_city_name}"],
            "site_zip9": [f"{ls_zip_cd}-{ls_zip4_cd}"],
            "site_phone_7": [f"{ls_phone[:7]}"],
            "site_phone_areacode": [f"{ls_ph_areacd}"],
            "site_state": [f"{ls_state_cd}"],
            "site_fax": None,
            "business_name": [f"{ls_org_name}"],
            # "original_source_and_ID": [f"{record['SRC_TP_CD']}:::{record['SRC_ID']}"],
            "site_zip4": [f"{ls_zip4_cd}"],
            "phone_number_most_frequent": [f"{ls_phone}"],
            "site_phone_full_number": [f"{ls_phone}"],
            "EMAIL": None,
            "site_phone_number_10dig": [f"{ls_phone}"],
            "COMPANY_NAME": [f"{ls_org_name}"],
            "site_phone_6": [f"{ls_phone[:6]}"],
            "ml_company_name": [f"{ls_org_name.replace(' ', '')}"],
            "ml_company_first_word": [f"{ls_org_name.split()[0]}"],
            "site_address_1_original": [f"{ls_addr1}"],
            "business_name_gr": [f"{ls_org_name}"]
        }
    }
    ls_org_id = "-1"
    ls_org_match_conf = "-1"
    try:
        response = requests.post(base_url, headers=headers, json=payload, timeout=30)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    print (response.status_code)

    if response.status_code == 200:
        lj_response = response.text.strip().splitlines()
        parsed = [json.loads(line) for line in lj_response if line.strip()]
        for d in parsed:
            # add new keys
            ls_org_id = d.get("clusterId")
            ls_org_match_conf = d.get("avgMatchProb")
    else:
        print(f"Error: {response.status_code} - {response.text}")

    return ls_org_id, ls_org_match_conf

def get_id_by_fields(req: AccountsRequest) -> tuple[int , bool, str]:
    org_id, org_match_conf = call_tamr_api(req)
    return org_id, True, "Record found"

    #     else:

    # sql = """
    # SELECT id
    #   FROM customer.curated.golden_record_company
    #  WHERE name      = nvl(%s,name)
    #    AND address1  = %s
    #    AND COALESCE(address2, '') = %s
    #    AND city      = %s
    #    AND state     = %s
    #    AND zip       = %s
    #    AND phone     = %s
    # LIMIT 1;
    # """
    # params = (
    #     req.accountName,
    #     req.address1,
    #     req.address2 or "",
    #     req.city,
    #     req.state,
    #     req.zip,
    #     req.phone,
    # )
    # conn = get_connection()
    # try:
    #     cur = conn.cursor()
    #     cur.execute(sql, params)
    #     row = cur.fetchone()
    #     if row:
    #         return row[0], True, "Record found"
    #     else:
    #         return None, False, "No matching record"
    # finally:
    #     cur.close()
    #     conn.close()

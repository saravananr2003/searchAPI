from .database import get_connection
from .schemas import LookupRequest

def get_id_by_fields(req: LookupRequest) -> tuple[int | None, bool, str]:
    sql = """
    SELECT id
      FROM customers
     WHERE name      = %s
       AND address1  = %s
       AND COALESCE(address2, '') = %s
       AND city      = %s
       AND state     = %s
       AND zip       = %s
       AND phone     = %s
    LIMIT 1;
    """
    params = (
        req.name,
        req.address1,
        req.address2 or "",
        req.city,
        req.state,
        req.zip,
        req.phone,
    )
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        row = cur.fetchone()
        if row:
            return row[0], True, "Record found"
        else:
            return None, False, "No matching record"
    finally:
        cur.close()
        conn.close()

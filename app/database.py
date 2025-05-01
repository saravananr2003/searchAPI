import snowflake.connector
from .config import settings

def get_connection():
    return snowflake.connector.connect(
        user=settings.user,
        password=settings.password,
        account=settings.account,
        warehouse=settings.warehouse,
        database=settings.database,
        schema=settings.schema,
        role=settings.role,
    )

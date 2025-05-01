import os
from dotenv import load_dotenv

load_dotenv()  # reads .env

class Settings:
    user        = os.getenv("SNOWFLAKE_USER")
    password    = os.getenv("SNOWFLAKE_PASSWORD")
    account     = os.getenv("SNOWFLAKE_ACCOUNT")
    warehouse   = os.getenv("SNOWFLAKE_WAREHOUSE")
    database    = os.getenv("SNOWFLAKE_DATABASE")
    schema      = os.getenv("SNOWFLAKE_SCHEMA")
    role        = os.getenv("SNOWFLAKE_ROLE")

    api_host    = os.getenv("API_HOST", "0.0.0.0")
    api_port    = int(os.getenv("API_PORT", 8000))

settings = Settings()

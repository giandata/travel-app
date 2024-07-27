from dotenv import dotenv_values
from pathlib import Path
from collections import namedtuple

dotenv_path = Path(__file__).resolve().parent.parent.parent / ".env"
dict = dotenv_values(dotenv_path=dotenv_path)

Env = namedtuple("env", ["OPENAPI_API_KEY"])

OPENAPI_API_KEY = dict.get("OPENAPI_API_KEY")
if OPENAPI_API_KEY is None:
    raise ValueError("[.env] OPENAPI_API_KEY is not valid.")

# Exposed
env = Env(OPENAPI_API_KEY)
from requests import get
from .client import Client


version = "1.5"
new = get("https://pypi.org/pypi/templus/json").json()["info"]["version"]
if version != new:
	print("A new version of templus has been released.")

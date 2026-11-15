import time
from tranco import Tranco

EMAIL = "deine@mail.de"
API_KEY = "DEIN_API_KEY"

t = Tranco(account_email=EMAIL, api_key=API_KEY, cache=True, cache_dir=".tranco")

config = {
    "providers": ["crux", "farsight", "majestic", "umbrella", "radar"],  # prüfen, welche aktuell gültig sind
    "startDate": "2026-10-01",
    "endDate": "2026-10-31",
    "combinationMethod": "dowdall",
    "listPrefix": 1000000,
    "filterPLD": "on",
    "filterTLD": "include",
    "filterTLDValue": ["de", "fr"],
}

available, list_id = t.configure(config)
print("Liste:", list_id)

# Warten, bis die Liste generiert ist
while not available:
    time.sleep(30)
    meta = t.list_metadata(list_id=list_id)
    available = meta["available"]
    if meta.get("failed"):
        raise RuntimeError("Listengenerierung fehlgeschlagen")

de_list = t.list(list_id=list_id)
for rank, domain in enumerate(de_list.top(), start=1):
    print(rank, domain)

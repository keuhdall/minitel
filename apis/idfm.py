import urequests as requests
import utime
from utils.utils import *

API_KEY = ""

ID_LINE_2_NATION = "STIF:StopPoint:Q:463088:"
ID_LINE_2_DAUPHINE = "STIF:StopPoint:Q:22114:"
ID_LINE_12_ISSY = "STIF:StopPoint:Q:463089:"
ID_LINE_12_AUBERVILLIERS = "STIF:StopPoint:Q:22040:"

def get_stations():
    return [
        {
            "id": ID_LINE_2_NATION,
            "line": "2",
            "direction": "Nation"
        },
        {
            "id": ID_LINE_2_DAUPHINE,
            "line": "2",
            "direction": "Porte Dauphine"
        },
        {
            "id": ID_LINE_12_ISSY,
            "line": "12",
            "direction": "Mairie D'Issy"
        },
        {
            "id": ID_LINE_12_AUBERVILLIERS,
            "line": "12",
            "direction": "Aubervilliers"
        }
    ]

def get_next_train(station_id):
    url = (
        "https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring"
        f"?MonitoringRef={station_id}"
    )
    headers = { "apiKey": API_KEY }
    try:
        r = requests.get(url, headers = headers)
        data = r.json()
        r.close()
        visits = data["Siri"]["ServiceDelivery"]["StopMonitoringDelivery"][0]["MonitoredStopVisit"]
        now = utime.time()
        delays = []
        for visit in visits:
            call = visit["MonitoredVehicleJourney"]["MonitoredCall"]
            ts = call.get("ExpectedDepartureTime") or call.get("ExpectedArrivalTime")

            if not ts:
                continue

            dep_ts = iso_to_unix(ts)
            delta = dep_ts - now

            if delta >= 0:
                delays.append(delta)

        if not delays:
            return None
        return min(delays)
    except:
        return None
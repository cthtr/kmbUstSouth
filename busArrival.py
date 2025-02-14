### DATETIME PARSING ONLY VALID ON WINDOWS, NOT LINUX ("%#I:%M %p")
### LINUX SOLUTION: ("%-I:%M %p")

import requests
from datetime import datetime, timezone
import pytz

class BusArrival:
    def __init__(this, route, timeString, timeTill, status):
        this.route = route # String
        this.timeString = timeString # String
        this.timeTill = timeTill # Integer
        this.status = status # int flag: -1 (no bus), 0 (final bus), 1
    
    def __repr__(this):
        return f"{this.route}: [No service / last bus has departed]" if this.status == -1\
        else f"Coming bus for Route {this.route}: {this.timeString} (in {this.timeTill} minutes){' [last bus]' if this.status == 0 else ''}"

## End of class definition

def getEtaData(stopId, timeDisplay = '24h'):
    arrivalObjs = []
    requestData = requests.get(f"https://data.etabus.gov.hk/v1/transport/kmb/stop-eta/{stopId}").json()

    for dataset in requestData['data']:

        routeString = dataset['route']
        if(dataset['eta'] == None): #final bus has departed
            arrivalObjs.append(BusArrival(routeString, -1, -1, -1))

        else:
            #handle ETA values
            etaLocal = datetime.fromisoformat(dataset['eta'])
            etaDisplayTime = etaLocal.strftime("%#I:%M%p") if timeDisplay == '12h' else etaLocal.strftime("%H:%M")
            currentEpoch = datetime.now().timestamp()
            etaEpoch = etaLocal.astimezone(pytz.utc).timestamp()
            timeTill = (int(etaEpoch) - int(currentEpoch))//60 #floor division: round DOWN to nearest integer (sec -> min)

            routeStatus = 0 if dataset['rmk_en'] == 'Final Bus' else 1

            arrivalObjs.append(BusArrival(routeString, etaDisplayTime, timeTill if timeTill >=0 else 0, routeStatus))

    return arrivalObjs

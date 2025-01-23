### DATETIME PARSING ONLY VALID ON WINDOWS, NOT LINUX ("%#I:%M %p")
### LINUX SOLUTION: ("%-I:%M %p")

import requests
import json
from datetime import datetime, timezone
import pytz
import time

class BusArrival:
  def __init__(this, route, timeString, timeTill, status):
    this.route = route
    this.timeString = timeString
    this.timeTill = timeTill
    this.status = status
  
  def __repr__(this):
    return f"{this.route}: [No service / last bus has departed]" if this.status == -1\
    else f"Coming bus for Route {this.route}: {this.timeString} (in {this.timeTill} minutes){' [last bus]' if this.status == 0 else ''}"

## End of class definition

def getEtaData(stopId, timeDisplay = '24h'):
  arrivalObjs = []
  requestData = requests.get("https://data.etabus.gov.hk/v1/transport/kmb/stop-eta/" + stopId).json()

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
      
      #determine route status
      # routeStatus = 1
      # if(dataset['rmk_en'] == 'Final Bus'): #final bus： set routeStatus to 0
      #   routeStatus = 0

      routeStatus = 0 if dataset['rmk_en'] == 'Final Bus' else 1

      arrivalObjs.append(BusArrival(routeString, etaDisplayTime, timeTill if timeTill >=0 else 0, routeStatus))

  return arrivalObjs

# busNow = getEtaData('B002CEF0DBC568F5') #91, 91M
# busSpecial = getEtaData('E9018F8A7E096544') # Special buses
# bus12h = getEtaData('B002CEF0DBC568F5', '12h') #91, 91M

# print(busNow, busSpecial, bus12h, sep='\n\n')

try:
  #busNow = getEtaData('B002CEF0DBC568F5')[1] #dictionary - key: bus route, value: list[('time', difference, status)]
  busNow = getEtaData('B002CEF0DBC568F5')
  nextArrival = []
  busTimes = []

  for key in busNow:
    print(f"key: {type(key)}")
finally:
  pass

bus91 = [r for r in busNow if r.route == '91']
bus91m = [r for r in busNow if r.route.upper() == '91M']
bus91.sort(key=lambda x: x.timeTill); bus91m.sort(key=lambda x: x.timeTill)

print(bus91m)
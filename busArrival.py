#code version: Jun 2024 / Cleaned up Sep 2024 for clarity
#there is an api get bug somewhere; I'm guessing it has something to do with a failure to get data at night.
#I have never run into that issue when using the widget during bus operating hours.

import requests
import json
from datetime import datetime, timezone
import pytz
import time

def getEtaData(stopId):
  timeSort = []
  routeSort = {}
  requestData = requests.get("https://data.etabus.gov.hk/v1/transport/kmb/stop-eta/" + stopId).json()
  for dataset in requestData['data']:

    arrData = 0
    routeString = dataset['route']

    if(dataset['eta'] == None): #final bus has departed

      timeSort.append((routeString, -1, -1, -1))
      arrData = (-1, -1, -1)
      routeSort[routeString] = [arrData]

    else:
      #handle ETA values
      etaLocal = datetime.fromisoformat(dataset['eta'])
      etaDisplayTime = "{:02d}:{:02d}".format(etaLocal.hour, etaLocal.minute) #display time, also local time

      currentEpoch = datetime.now().timestamp()
      etaEpoch = etaLocal.astimezone(pytz.utc).timestamp()

      timeTill = (int(etaEpoch) - int(currentEpoch))//60 #floor division: round DOWN to nearest integer
      
      #determine route status
      routeStatus = 1
      if(dataset['rmk_en'] == 'Final Bus'): #final bus case (set routeStatus to 0)
        routeStatus = 0

      #append tuple: (route, eta, eta_countdown, status)
      if timeTill >= 0:
        timeSort.append((routeString, etaDisplayTime, timeTill, routeStatus))
        if routeString in routeSort:
          routeSort[routeString].append((etaDisplayTime, timeTill, routeStatus))
        else:
          routeSort[routeString] = [(etaDisplayTime, timeTill, routeStatus)]

  timeSort.sort(key = lambda x: x[2])
  return(timeSort, routeSort)

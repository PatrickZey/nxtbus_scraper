import requests
from dataclasses import dataclass, field
import json
import time
import math

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@dataclass
class Bounds:
    left: float
    right: float
    top: float
    bottom: float
    

@dataclass(order=True)
class BusStop:
    sort_index: float = field(init=False, repr=False)
    
    name: str
    number: str
    id: str
    latitude: float
    longitude: float
    
    def __post_init__(self):
        self.sort_index = self.latitude

def getStops(bounds):
    url = 'http://www.nxtbus.act.gov.au/visibleLookupRequest'
    
    left = str(bounds.left)
    right = str(bounds.right)
    top = str(bounds.top)
    bottom = str(bounds.bottom)
    postData = {
        'center': {
            'latitude': 1, 
            'longitude': 1
        }, 
        'lowerLeft': {
            'latitude': bottom, 
            'longitude': left
        }, 
        'upperRight': {
            'latitude': top, 
            'longitude': right
        }
    }

    response = requests.post(url, json = postData)
    result = response.json()['status']
    if not result == 'SUCCESS':
        raise ConnectionError('Nxtbus server connection failed')
    return response.json()['body']

def main():
    allStops = []
    width = 0.005841797911134
    height = 0.01701593399047
    
    canberraBounds = Bounds(
            148.97608977854566,
            149.21671463557652,
            -35.13581822607829,
            -35.483867730579036
    )
    
    
    bounds = Bounds(
        canberraBounds.left,
        canberraBounds.left + width,
        canberraBounds.top,
        canberraBounds.top - height
        )
        
    canberraHeight = canberraBounds.top - canberraBounds.bottom
    
    while bounds.top > canberraBounds.bottom:
        while bounds.left < canberraBounds.right:
            stops = getStops(bounds)
            print("Found {count} stops in region: {bounds}".format(count = len(stops), bounds = bounds))
            for stop in stops:
                name = stop['name']
                id = stop['id']
                lat = float(stop['coordinate']['latitude'])
                long = float(stop['coordinate']['longitude'])
                
                numStart = name.find('[') + 1
                numEnd = name.find(']', numStart)
                number = name[numStart:numEnd]
                name = name[0:numStart - 2]
                
                stop = BusStop(name, number, id, lat, long)
                allStops.append(stop)
                
            time.sleep(0.2) # I don't want to swamp their server
            bounds.left += width
            bounds.right += width
        bounds.top -= height
        bounds.bottom -= height
        bounds.left = canberraBounds.left
        bounds.right = canberraBounds.left + width
        print("{blue}{percent}% DONE{norm}".format(blue = bcolors.OKBLUE, percent = ((bounds.bottom / canberraHeight) * -1 - 101) * 100, norm=bcolors.ENDC))
        
    allStops = sorted(allStops, reverse = True)
        
    f = open("stops.csv", "w")
    f.write("Updated: {time}\n".format(time = int(time.time_ns() / 1000000)))
    f.write("Count: {count}\n".format(count = len(allStops)))
    f.write("name,number,id,latitude,longitude\n")
    for stop in allStops:
        f.write("{name},{number},{id},{lat},{long}\n".format(
                name = stop.name,
                number = stop.number,
                id = stop.id,
                lat = stop.latitude,
                long = stop.longitude
        ))
    f.close()


if __name__ == "__main__":
    main()
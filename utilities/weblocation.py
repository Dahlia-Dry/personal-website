from core.models import *
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='website')

def yaml_to_dict(fname = 'locations.yaml'):
    y = open(fname,'r')
    data=y.read()
    entries = [x.split('\n') for x in data.split('---')]
    location_data = {}
    for entry in entries[1:-1]:
        loc = {}
        for line in entry[1:-1]:
            yaml=line.split(':')
            if len(yaml)!=2:
                continue
            loc[yaml[0].strip()] = yaml[1].strip()
        location_data[loc.pop('name')]=loc
    y.close()
    return location_data

def dict_to_yaml(dict,fname= 'locations.yaml'):
    y=open(fname,'w')
    y.write('---\n')
    for name in dict:
        y.write(f'name : {name}\n')
        for attr in dict[name]:
            y.write(f'{attr} : {dict[name][attr]}\n')
        y.write('---\n')
    y.close()

class webLocation(object):
    def __init__(self,name,address=None,coords=None):
        """
        name: str, title of location
        address: str, address of location
        coords: tuple (lat,long) of location coordinates
        """
        self.name=name
        if address is not None:
            try:
                loc = geolocator.geocode(address)
            except:
                raise Exception(f"Error at {self.name}:Location {address} not found :(")
            else:
                if loc is not None:
                    self.address=loc.address
                    self.coords = (loc.latitude,loc.longitude)
                else:
                    self.address = address
                    self.coords = coords
        elif coords is not None:
            try:
                loc=geolocator.reverse(coords)
            except:
                raise Exception(f"Error at {self.name}:coords {coords} not found :(")
            else:
                self.address=loc
                self.coords=coords
        else:
            raise Exception('either coords or address must be specified.')
    def update_yaml(self,fname='locations.yaml'):
        yaml = yaml_to_dict(fname)
        yaml[self.name] = {}
        yaml[self.name]['address'] =self.address
        yaml[self.name]['coords'] =self.coords
        dict_to_yaml(yaml,fname)
        print(f'{fname} updated.')
    def register_as_Location(self):
        try:
            instance=Location.objects.get(name=self.name)
        except: #create new
            instance=Location.objects.create(name=self.name,
                                             lat=self.coords[0],long=self.coords[1],
                                             address=self.address)
            instance.save()
            print(f"{self.name} added to Location db")
        return instance


        


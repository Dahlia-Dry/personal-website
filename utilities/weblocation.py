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
        self.yaml = yaml_to_dict()
        if address is not None:
            self.address = address
            if 'coords' not in self.yaml[self.name]:
                try:
                    loc = geolocator.geocode(address)
                except:
                    loc = None
                else:
                    if loc is not None:
                        self.address=loc.address
                        self.coords = (loc.latitude,loc.longitude)
                        self.yaml[self.name]['address'] = self.address
                        self.yaml[self.name]['coords'] = self.coords
                    else:
                        self.coords = coords
        elif coords is not None:
            self.coords = coords
            if 'address' not in self.yaml[self.name]:
                try:
                    loc=geolocator.reverse(coords)
                except:
                    raise Exception(f"Error at {self.name}:coords {coords} not found :(")
                else:
                    if loc is not None:
                        self.address=loc
                        self.yaml[self.name]['address']=self.address
        else:
            raise Exception('either coords or address must be specified.')
        dict_to_yaml(self.yaml)
    def update_yaml(self,fname='locations.yaml'):
        self.yaml[self.name] = {}
        self.yaml[self.name]['address'] =self.address
        self.yaml[self.name]['coords'] =self.coords
        dict_to_yaml(self.yaml,fname)
        print(f'{fname} updated.')
    def register_as_Location(self):
        try:
            instance=Location.objects.get(name=self.name)
        except: #create new
            try:
                instance=Location.objects.create(name=self.name,
                                                lat=self.coords[0],long=self.coords[1],
                                                address=self.address)
            except:
                instance=Location.objects.create(name=self.name,
                                                address=self.address)
            instance.save()
            print(f"{self.name} added to Location db")
        return instance


        


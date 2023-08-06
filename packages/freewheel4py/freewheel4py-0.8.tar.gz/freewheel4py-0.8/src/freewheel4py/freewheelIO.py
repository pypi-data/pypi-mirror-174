import requests as rs
import xmltodict
from dict2xml import dict2xml
class freewheel_auth():
    def __init__(self,username,password):
        try:
            filetype = 'xml'
            headers = {'accept': 'application/json','content-type': 'application/x-www-form-urlencoded',}
            data = { 'grant_type': 'password','username': username,'password': password,}
            response = rs.post('https://api.freewheel.tv/auth/token', headers=headers, data=data).json()
            response['access_token']
            token = 'Bearer ' + response['access_token']
            headers = {'accept': 'application/'+str(filetype), 'authorization' : token, 'Content-Type': 'application/'+str(filetype),} 
            self.xml = headers
            filetype = 'json'
            headers = {'accept': 'application/json','content-type': 'application/x-www-form-urlencoded',}
            data = { 'grant_type': 'password','username': username,'password': password,}
            response = rs.post('https://api.freewheel.tv/auth/token', headers=headers, data=data).json()
            response['access_token']
            token = 'Bearer ' + response['access_token']
            headers = {'accept': 'application/'+str(filetype), 'authorization' : token, 'Content-Type': 'application/'+str(filetype),} 
            self.json = headers
        except JSONDecodeError:
            raise Exception('Invalid Credentials')
            
class FreewheelIO():
    def __init__(self,freewheel_auth,Name,ID):
        fw = freewheel_auth
        if Name =='API':
            ioGet = xmltodict.parse(rs.get(f"https://api.freewheel.tv/services/v3/insertion_orders/{ID}",headers = fw.xml).text,dict_constructor = dict)
            Name = ioGet['insertion_order']['name']
            camp = ioGet['insertion_order']['campaign_id']
            self.freewheel_auth = freewheel_auth
            self.Name = Name
            self.campaignID = camp
            self.ID = ID
        else:

            self.freewheel_auth = freewheel_auth
            self.Name=  Name
            self.ID = ID
            
    def GetPlacements(self):
        fw = self.freewheel_auth
        placeUrl = f"https://api.freewheel.tv/services/v3/insertion_order/{self.ID}/placements?per_page=50&page=1"
        placeGet = xmltodict.parse(rs.get(placeUrl,headers = fw.xml).text,dict_constructor = dict)
        numberOfPages = int(placeGet['placements']['@total_pages'])
        placementList = []
        for i in range(numberOfPages):
            placeUrlLoop = f"https://api.freewheel.tv/services/v3/insertion_order/{self.ID}/placements?per_page=50&page={i+1}"
            placeGetLoop = xmltodict.parse(rs.get(placeUrlLoop,headers = fw.xml).text,dict_constructor = dict)
            print(placeGetLoop['placements']['placement'])
            
            if type(placeGetLoop['placements']['placement']) == dict:
                placement = FreewheelPlacement(Name = placeGetLoop['placements']['placement']['name'], PID = placeGetLoop['placements']['placement']['id'])
                placementList.append(placement)
            else:

                for item in placeGetLoop['placements']['placement']:

                    placement = FreewheelPlacement(Name = item['name'], PID = item['id'])
                    placementList.append(placement)

        self.placementList = placementList

        placementDict = {}
        for item in placementList:
            placementDict[item.Name] = item.PID

        self.placementDict = placementDict
        
    def runPlacementForecast(self):
        fw = self.freewheel_auth
        self.GetPlacements()
        counter = 0
        for item in self.placementList:
            counter = counter + 1
            print(counter)
            item.runForecast(self)
                
            
            
class FreewheelPlacement():
    def __init__(self,Name, PID):
        self.PID = PID
        self.Name = Name
        
    def runForecast(self,FreewheelIO):
        fw = FreewheelIO.freewheel_auth
        url = f"https://api.freewheel.tv/services/v4/placements/{self.PID}/forecasts"
        forecastPost = rs.post(url,headers = fw.json).json()
        try:
            self.forecastParams = f"https://api.freewheel.tv/services/v4/placements/{self.PID}/forecasts?forecast_id={forecastPost['job_id']}"
        except KeyError:
            print(forecastPost)
            
def getForecast(url,freewheel_auth):
    fw = freewheel_auth
    get = rs.get(url,headers = fw.json).json()
    
    return get

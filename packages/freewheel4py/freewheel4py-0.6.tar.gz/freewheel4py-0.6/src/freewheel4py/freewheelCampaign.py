class fw():
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

class insertionOrderObj():
    def __init__(self ,**kwargs):
        dictObj  = {}
        for key, value in kwargs.items():
            
            dictObj[key] = value
            
        self.placements = []
        self.data = {'insertion_order' : dictObj}
    
        
    def Get(self,fw):
        
        try:
            url = f"https://api.freewheel.tv/services/v3/insertion_orders/{self.data['insertion_order']['id']}"
        except KeyError:
            raise insertionOrderMissingIdError('''insertion order is missing ID from its data''')
            
        
        
        
        ioGet = xmltodict.parse(rs.get(url,headers = fw.xml).text,dict_constructor = dict)
        
        self. data = ioGet
        
    def GetPlacements(self,fw):
        placeUrl = f"https://api.freewheel.tv/services/v3/insertion_order/{self.data['insertion_order']['id']}/placements?per_page=50&page=1"
        placeGet = xmltodict.parse(rs.get(placeUrl,headers = fw.xml).text,dict_constructor = dict)
        numberOfPages = int(placeGet['placements']['@total_pages'])
        
        
        for i in range(numberOfPages):
            placeUrlLoop = f"https://api.freewheel.tv/services/v3/insertion_order/{self.data['insertion_order']['id']}/placements?per_page=50&page={i+1}"
            placeGetLoop = xmltodict.parse(rs.get(placeUrlLoop,headers = fw.xml).text,dict_constructor = dict)

            
            if type(placeGetLoop['placements']['placement']) == dict:
                placement = placementObj(id = placeGetLoop['placements']['placement']['id'])
                placement.Get(fw)
                self.placements.append(placement)
                
            else:

                for item in placeGetLoop['placements']['placement']:
                    placement = placementObj( id = item['id'])
                    placement.Get(fw)
                    self.placements.append(placement)
                    

class insertionOrderError(Exception):
     pass
    
class insertionOrderMissingIdError(Exception):
     pass


class placementObj():
    def __init__(self ,**kwargs):
        dictObj  = {}
        for key, value in kwargs.items():
            
            dictObj[key] = value
            

        self.data = {'placement' : dictObj}
        
        
    def Get(self,fw):
        node = 'all'
        try:
            get_url = f"https://api.freewheel.tv/services/v3/placements/{self.data['placement']['id']}?show={node}"
        except KeyError:
            raise placementMissingIdError('''placement is missing ID from its data''')
        get_placement = rs.get(get_url,headers=fw.xml).text
        self.data = xmltodict.parse(get_placement,dict_constructor=dict)
        
    def runForecast(self,fw):
        try:
            url = f"https://api.freewheel.tv/services/v4/placements/{self.data['placement']['id']}/forecasts"
        except KeyError:
            placementMissingIdError('''placement is missing ID from its data''')
        
            
        forecastPost = rs.post(url,headers = fw.json).json()
    
        try:
            forecastPost['job_id']
        except KeyError:
            if "A forecast for this item is already processing." != forecastPost['errors'][0]['message']:
                message = f"placement is Missing {forecastPost['errors'][0]['message'][75:-1]}"
                raise placementMissingForecastItemError(f'''{message}''')
            elif "A forecast for this item is already processing." == forecastPost['errors'][0]['message']:
                raise placementForecastHasNotLoadedError('''forecast is still processing wait until it has finished to run again''')
            
        self.forecastUrl = f"https://api.freewheel.tv/services/v4/placements/{forecastPost['placement_id']}/forecasts?forecast_id={forecastPost['job_id']}"
    
    def getForecast(self,fw)
        try:
            forecastGet = rs.get(self.placements[2].forecastUrl,headers = fw.json).json()
        except AttributeError:
            placementMissingJobIdError(Exception)
            
        try:
            forecastGet['net_available']
        except KeyError:
            if self.data['placement']['id'] in forecastGet['errors'][0]['message'] and Please try again later. in ['errors'][0]['message']:
                raise placementForecastResultsNotReadyError('''forecast is not ready yet, try later when it has loaded.''')
                
        self.forecastResults = forecastGet
        


        
class placementError(Exception):
     pass
    
class placementMissingIdError(Exception):
     pass
    
class placementMissingForecastItemError(Exception):
     pass
    
class placementForecastProcessingError(Exception):
     pass
    
class placementMissingJobIdError(Exception):
     pass
    
class placementForecastResultsNotReadyError(Exception):
     pass

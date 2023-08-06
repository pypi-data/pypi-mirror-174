import requests as rs
import json
from json import JSONDecodeError
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
            
class creativeObj():
    def __init__(self ,**kwargs):
        dictObj  = {}
        for key, value in kwargs.items():
            
            dictObj[key] = value
            
        self.rendition = []
        self.data = {'creative' : dictObj}

    def pushCreative (self,fw):
        url = 'https://api.freewheel.tv/services/v4/creative_resources'
        
        post = rs.post(url,headers =fw.json, data = json.dumps(self.data)).json()
        
        self.data['creative']['id'] = post['data']['creative']['id']
        self.id = post['data']['creative']['id']
        rendition = []
        for i in range (len(post['data']['renditions'])):
            rend = renditionObj()
            rend.data = self.rendition[i]
            rend.id = post['data']['renditions'][i]['id']
            rendition.append(rend)
        self.rendition = rendition
                
        return post 
    
    def getCreative(self,fw):
        try:
            url = f'https://api.freewheel.tv/services/v4/creative_resources/{self.id}?include=renditions'
        except AttributeError:

            raise creativeIdError("""creativeObj has not been pushed to Freewheel""")
        
        get= rs.get(url,headers = fw.json).json()
        return get
    
class renditionObj ():
    
    def __init__(self,creativeObj = None, **kwargs):      
        dictObj = {}       
        for key, value in kwargs.items():
            dictObj[key] = value
                   
        if creativeObj is not None:    
            creativeObj.rendition.append(dictObj)
            creativeObj.data['creative']['renditions'] = creativeObj.rendition
        elif creativeObj is None:
            self.data =dictObj
            
    def renditionUpdate(self,fw):    
        putUrl = f'https://api.freewheel.tv/services/v4/creative_renditions/{self.id}'
        putReq = rs.put(putUrl,headers = fw.json,data = json.dumps(self.data)).json()
        return putReq
        
        
class creativeQueryError(Exception):
     pass
    
class creativeQueryInvalidDateError(Exception):
     pass
    

def creativeQuery(fw,**kwargs):
    queryParams = {'created_at' :'created_at', 
        'updated_at' : 'updated_at',
                   
        'include' : 'renditions'}
    urlQuery = "&"
    for key, value in kwargs.items():
        try:    
            if key == 'created_at':
                try:
                    json.loads(value)
                except JSONDecodeError:
                    raise creativeQueryInvalidDateError('''created at query is not correct''')
                urlQuery = urlQuery + f'{key}={value}&'
            elif key == 'updated_at':
                try:
                    json.loads(value)
                except JSONDecodeError:
                    raise creativeQueryInvalidDateError('''updated at query is not correct''')
                urlQuery = urlQuery + f'{key}={value}&'
            elif key == 'include':
                urlQuery = urlQuery + f'{key}={queryParams[key]}&'
        except KeyError:
            raise creativeQueryError('''Keyword is not a valid query
    valid queries are created_at,updated_at, ad_unit_id ''')
    url ='https://api.freewheel.tv/services/v4/creative_resources?per_page=50&page=1' + urlQuery
    url = url + 'REPLACE'    
    queryUrl = url.replace('&REPLACE',"")  
    getQuery =rs.get(queryUrl,headers=FW.json).json()  
    creativeList = []
    for item in getQuery['items']:
        creative = cleanCreative(item)
        for rend in item['renditions']:
            creative.rendition.append(cleanRendition(rend))          
    creativeList.append(creative)  
    return creativeList

def cleanCreative(item):

    creative= creativeObj()
    creative.id = item['id']
    creative.Created = item['created_at']
    creative.Updated= item['updated_at']

    del item['id']
    del item['updated_at']
    del item['created_at']

    newDict= {}
    for key in item.keys():
        if item[key] is not None:
            newDict[key] = item[key]

    creative.data= newDict
    
    return creative

def cleanRendition(item):
    creative= creativeObj()
    newDict= {}
    for key in item.keys():
        if item[key] is not None:
            newDict[key] = item[key]
        
    rend = renditionObj()
    rend.data = newDict
    
    return rend
        
class creativeIdError(Exception):
     pass

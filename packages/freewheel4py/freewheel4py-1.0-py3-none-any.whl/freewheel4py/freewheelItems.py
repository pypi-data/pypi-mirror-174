import requests as rs
import json
import xmltodict

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
            
            
            
            
    def getFreewheelItems(self, ITEM):
        
        url = f'https://api.freewheel.tv/services/v4/{ITEM}?per_page=500&page=1'
        getUrl = rs.get(url,headers = self.json).json()
        siteDict = {}
        for i in range(getUrl['total_page']):
            getUrl = rs.get(f"https://api.freewheel.tv/services/v4/{ITEM}?per_page=500&page={i+1}",headers =self.json).json()
            for item in getUrl['items']:
                siteDict[item['id']] =  item['name']

        return siteDict
    
    def getFreewheelAudienceItems(self):
        url = 'https://api.freewheel.tv/services/v4/audience_items?per_page=100&page=1'
        getUrl = rs.get(url,headers =self.json).json()['audience_items']
        siteDict = {}
        for i in range(getUrl['total_page']):
            getUrl = rs.get(f"https://api.freewheel.tv/services/v4/audience_items?per_page=100&page={i+1}",headers =self.json).json()['audience_items']
            for item in getUrl['items']:
                siteDict[item['id']] =  item['name']

        return siteDict
    
    def getFreewheelAdUnits(self):
        
        url = 'https://api.freewheel.tv/services/v4/ad_units?per_page=100&page=1'
        getUrl = rs.get(url,headers =self.json).json()
        siteDict = {}
        for i in range(getUrl['total_pages']):
            getUrl = rs.get(f"https://api.freewheel.tv/services/v4/ad_units?per_page=100&page={i+1}",headers =self.json).json()
            for item in getUrl['ad_units']:
                siteDict[item['id']] =  item['name']

        return siteDict
    
    def getAdveristerBrands(self):
        url = 'https://api.freewheel.tv/services/v3/advertisers?per_page=100&page=54'
        advDict = {}
        getUrl = xmltodict.parse(rs.get(url,headers=self.xml).text,dict_constructor = dict)
        totalPage = int(getUrl['advertisers']['@total_pages'])
        for i in range(totalPage):
            url = f'https://api.freewheel.tv/services/v3/advertisers?per_page=100&page={i+1}'
            getUrl = xmltodict.parse(rs.get(url,headers=self.xml).text,dict_constructor = dict)
            for adv in getUrl['advertisers']['advertiser']:
                brandUrl = f"https://api.freewheel.tv/services/v3/advertisers/{advertiser_id}/brands?per_page=100"
                brandList  =  xmltodict.parse(rs.get(brandUrl,headers=self.xml).text,dict_constructor = dict)['brands']['brand']
                brandDict = {brand['id'] :  brand['name'] for brand in brandList}
                advDict[adv['id']] = {'name' :adv['name'] , 'brands' : brandDict}
                
        return advDict

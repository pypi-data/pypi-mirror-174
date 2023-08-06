# import io
# import json
# from io import StringIO
# from json import JSONDecodeError
# from pathlib import Path
# import boto3
# import pandas as pd
# import requests as rs
# import xmltodict
# from dict2xml import dict2xml




# import io
# import json
# from io import StringIO
# from json import JSONDecodeError
# from pathlib import Path
# import boto3
# import pandas as pd
# import requests as rs
# import xmltodict
# from dict2xml import dict2xml


# class freewheel_auth():
#     def __init__(self,username,password):
#         try:
#             filetype = 'xml'
#             headers = {'accept': 'application/json','content-type': 'application/x-www-form-urlencoded',}
#             data = { 'grant_type': 'password','username': username,'password': password,}
#             response = rs.post('https://api.freewheel.tv/auth/token', headers=headers, data=data).json()
#             response['access_token']
#             token = 'Bearer ' + response['access_token']
#             headers = {'accept': 'application/'+str(filetype), 'authorization' : token, 'Content-Type': 'application/'+str(filetype),} 
#             self.xml = headers
#             filetype = 'json'
#             headers = {'accept': 'application/json','content-type': 'application/x-www-form-urlencoded',}
#             data = { 'grant_type': 'password','username': username,'password': password,}
#             response = rs.post('https://api.freewheel.tv/auth/token', headers=headers, data=data).json()
#             response['access_token']
#             token = 'Bearer ' + response['access_token']
#             headers = {'accept': 'application/'+str(filetype), 'authorization' : token, 'Content-Type': 'application/'+str(filetype),} 
#             self.json = headers
#         except JSONDecodeError:
#             raise Exception('Invalid Credentials')
            
# class PlacementStringQuery():
    
#     def __init__(self,freewheel_auth,query,Dict = None):
#         self.freewheel_auth = freewheel_auth
#         headers = self.freewheel_auth.xml
#         get = rs.get(f"https://api.freewheel.tv/services/v3/placements?name={query}&status=ACTIVE&per_page=50&page=1",headers=headers).text
#         get = xmltodict.parse(get,dict_constructor = dict)
#         placements = get['placements']['placement']
#         listy = []
#         pids = []
#         pages = int(get['placements']['@total_pages'])
#         for i in range(pages):
#             get = rs.get(f"https://api.freewheel.tv/services/v3/placements?name={query}&status=ACTIVE&per_page=50&page={i+1}",headers=headers).text
#             get = xmltodict.parse(get,dict_constructor = dict)
#             placements = get['placements']['placement']
#             for item in placements:
#                 if Dict.lower() == 'yes':
#                     PID = item['id']
#                     pids.append(PID)
#                     attach = {'attach' : 'Yes', "PID" : PID}
#                     placement = Placement(freewheel_auth = fw,attach = attach)
#                     placement.Get()
#                     listy.append(placement.dict)
#                 else:
#                     PID = item['id']
#                     pids.append(PID)
#                     attach = {'attach' : 'Yes', "PID" : PID}
#                     placement = Placement(freewheel_auth = fw,attach = attach)
#                     placement.Get()
#                     listy.append(placement)

        
#         self.PIDs = pids           
#         self.list = listy
        

        
        
        
#     def GetPacing(self):
        
#         nightly = []
#         headers = self.freewheel_auth.json
#         for item in query.PIDs:
#             url = f'https://api.freewheel.tv/services/v4/placements/{item}/forecasts?type=nightly'
#             get = rs.get(url,headers=headers).json()
#             nightly.append(get)
            
#         self.Pacing = nightly
        
        
        
#     def ExportJSONToS3(self,S3Auth):
#         S3Auth.s3c.put_object(
#          Body=json.dumps(self.list),
#          Bucket=S3Auth.bucketName ,
#          Key=S3Auth.bucketKey)
        
# class PacingSnapShot():
    
#     def __init__(self,PlacementStringQuery):
    
#         PlacementStringQuery.GetPacing()
#         pacing_dict = {}
#         for i in range(len(query.list)):
#             budget = query.Pacing[i]['budget']
    
#             if ',' in budget:
#                 budget = int("".join(query.Pacing[i]['budget'].replace('imps', '').replace(' ', "").split(',')))
#             else:
#                 budget = int(budget)
                
#             try:
                
#                 start = PlacementStringQuery.list[i]['placement']['schedule']['start_time']
#                 end = PlacementStringQuery.list[i]['placement']['schedule']['end_time']
                
#             except KeyError:
#                 start = 'None'
#                 end  = 'None'
        
#             pacing_dict[query.list[i]['placement']['name']] = {'OSI' : query.Pacing[i]['on_schedule_indicator']/100,
#     'FFDR': query.Pacing[i]['forecast_final_delivery_rate']/100,
#     'grossDeliveredImps' : query.Pacing[i]['delivered_impressions'],
#     'budgetedImps' : budget,
#     'startDate': start, 'endDate': end}
            
            
#             self.SnapShot = pacing_dict
            
#     def ExportToCSV(self,path):

#         df = pd.DataFrame()
#         name_list = []
#         osi_list = []
#         ffdr_list = []
#         g_imps = []
#         b_imps = []
#         start_list = []
#         end_list = []

#         for item in self.SnapShot.keys():
#             name_list.append(item)
#             start_list.append(self.SnapShot[item]['startDate'])
#             end_list.append(self.SnapShot[item]['endDate'])
#             osi_list.append(self.SnapShot[item]['OSI'])
#             ffdr_list.append(self.SnapShot[item]['FFDR'])
#             g_imps.append(self.SnapShot[item]['grossDeliveredImps'])
#             b_imps.append(self.SnapShot[item]['budgetedImps'])

#         df['placementName'] = name_list
#         df['placementStartDate']  = start_list
#         df['placementEndDate'] = end_list
#         df['placementOSI'] = osi_list
#         df['placementFFDR'] = ffdr_list
#         df['placementGrossDeliveredImpressions'] = g_imps
#         df['PlacementBudgetedImpressions'] = b_imps

#         df.to_csv(path,index=False)
#         print('pushedToCSV')

#     def ExportToJSON(self,path):

#         file = open(path,'w')
#         file.write(json.dumps(self.SnapShot))
#         file.close()


#         print('pushedToJSON')
        
        
#     def ExportJSONToS3(self,S3Auth):
#         S3Auth.s3c.put_object(
#          Body=json.dumps(self.SnapShot),
#          Bucket=S3Auth.bucketName ,
#          Key=S3Auth.bucketKey)
        
#     def ExportCSVToS3(self,S3Auth):        
#         df = pd.DataFrame()
#         name_list = []
#         osi_list = []
#         ffdr_list = []
#         g_imps = []
#         b_imps = []
#         start_list = []
#         end_list = []

#         for item in self.SnapShot.keys():
#             name_list.append(item)
#             start_list.append(self.SnapShot[item]['startDate'])
#             end_list.append(self.SnapShot[item]['endDate'])
#             osi_list.append(self.SnapShot[item]['OSI'])
#             ffdr_list.append(self.SnapShot[item]['FFDR'])
#             g_imps.append(self.SnapShot[item]['grossDeliveredImps'])
#             b_imps.append(self.SnapShot[item]['budgetedImps'])

#         df['placementName'] = name_list
#         df['placementStartDate']  = start_list
#         df['placementEndDate'] = end_list
#         df['placementOSI'] = osi_list
#         df['placementFFDR'] = ffdr_list
#         df['placementGrossDeliveredImpressions'] = g_imps
#         df['PlacementBudgetedImpressions'] = b_imps
        
#         csv_buffer = StringIO()
#         df.to_csv(csv_buffer,index = False)
#         S3Auth.s3r.Object(S3Auth.bucketName,S3Auth.bucketKey).put(Body=csv_buffer.getvalue())
        
        
    
    
                    

    
    
        
# class Placement():
#     def __init__(self,freewheel_auth,IO= None,attach= None):
#         try:
#             if attach['attach'] ==  'Yes':
#                 self.freewheel_auth = freewheel_auth
#                 headers = self.freewheel_auth.xml
#                 self.PID = attach['PID'] 
#                 node = 'all'
#                 get_url = f'https://api.freewheel.tv/services/v3/placements/{str(self.PID)}?show={node}'
#                 get_placement = rs.get(get_url,headers=headers).text
#                 self.dict = xmltodict.parse(get_placement,dict_constructor=dict)
#                 self.Name  = self.dict['placement']['name']
#             elif attach['attach'] == 'No':

#                 try:
#                     self.freewheel_auth = freewheel_auth
#                     self.IO = IO
#                 except:
#                     raise Exception("invalid username or password")
                
#         except:
#             raise Exception("invalid username or password")
                
            

        
        
#     def Get(self):

#         PID = self.PID
#         headers = self.freewheel_auth.xml
#         node = 'all'
#         get_url = f'https://api.freewheel.tv/services/v3/placements/{str(PID)}?show={node}'
#         get_placement = rs.get(get_url,headers=headers).text
#         self.dict = xmltodict.parse(get_placement,dict_constructor=dict)
#         self.aud =self.dict['placement']['audience_targeting']
#         self.content = self.dict['placement']['content_targeting']
# #             include = 'include'
# #             exclude = 'exclude'
# #             self.contentInclusions= self.dict['placement']['content_targeting'][include]
# #             self.contentExclusions = self.dict['placement']['content_targeting'][exclude]
# #             self.sets = self.contentInclusions['set']
# #             self.numberOfSets = len(self.contentInclusions['set'])
# #             try:
# #                 self.exclusionFwItems = list(self.contentExclusions.keys())
# #             except AttributeError:
# #                 self.exclusionFwItems = 'None'

# #             try:
# #                 keys = list(self.sets.keys())
# #                 for item in keys:
# #                     print(item)
# #                 self.set = self.sets
# #                 self.numberOfsets = 1
# #             except AttributeError:

# #                 keys = self.sets

# #                 if len(keys) == 3:
# #                     self.setOne = keys[0]
# #                     self.setOneFwItems = list(keys[0].keys())
# #                     self.setTwo = keys[1]
# #                     self.setTwoFwItems = list(keys[1].keys())
# #                     self.setThree = keys[2]
# #                     self.setThreeFwItems = list(keys[2].keys())
# #                 if len(keys) ==2: 
# #                     self.setOne = keys[0]
# #                     self.setOneFwItems =list(keys[0].keys())               
# #                     self.setTwo = keys[1]
# #                     self.setTwoFwItems = list(keys[1].keys())
# #         except KeyError:
# #             PID = self.PID
# #             headers = self.freewheel_auth.xml
# #             node = 'all'
# #             get_url = f'https://api.freewheel.tv/services/v3/placements/{str(PID)}?show={node}'
# #             get_placement = rs.get(get_url,headers=headers).text
# #             self.dict = xmltodict.parse(get_placement,dict_constructor=dict)
                


            

#     def Create(self,Name):
#         headers = self.freewheel_auth.xml
#         IO = self.IO
#         placement = {}
#         placement['placement'] = {'insertion_order_id' : IO}
#         placement['placement']['name'] = Name
#         createpid = rs.post('https://api.freewheel.tv/services/v3/placement/create',headers=headers,data=dict2xml(placement))
#         pid = xmltodict.parse(createpid.text,dict_constructor=dict)['placement']['id']
#         self.PID = pid
#         self.Name = Name
    

        
    
    
# class FreewheelAudience():
#     def __init__(self,Name,ID):
        
#         self.Name = Name
#         self.ID = ID
# class FreewheelAudienceList():
#     def __init__(self,freewheel_auth):
    
#         fw = freewheel_auth
#         url = f'https://api.freewheel.tv/services/v4/audience_items?status=ACTIVE&page=1&per_page=100'
#         get = rs.get(url,headers = fw.json).json()

#         audience_list = []
#         numberOfPages = get['audience_items']['total_page']

#         for i in range(numberOfPages):
#             url = f'https://api.freewheel.tv/services/v4/audience_items?status=ACTIVE&page={i+1}&per_page=100'
#             get = rs.get(url,headers = fw.json).json()
#             for item in get['audience_items']['items']:
#                 FWA = FreewheelAudience(Name = item['name'], ID = item['id'])
#                 audience_list.append(FWA)
                
#         self.list = audience_list
        
        
#     def ToDict(self):
#         dicty = {}
#         for item in self.list:
#             dicty[item.Name] = item.ID
            
#         self.dict = dicty
        
#     def ExportToCSV(self,path):
#         self.ToDict()
#         df = pd.DataFrame()
        
#         df['audienceName'] = self.dict.keys()
#         df['audienceId'] = self.dict.values()
#         df.to_csv(path,index = False)
        
#     def ExportToJSON(self,path):
#         self.ToDict()
#         file = open(path,'w')
#         file.write(json.dumps(self.dict))
#         file.close()
        
#     def ExportJSONToS3(self,S3Auth):
#         self.ToDict()
#         S3Auth.s3c.put_object(
#          Body=json.dumps(self.dict),
#          Bucket=S3Auth.bucketName ,
#          Key=S3Auth.bucketKey)
        
#     def ExportCSVToS3(self,S3Auth):        
#         self.ToDict()
#         df = pd.DataFrame()
#         df['audienceName'] = self.dict.keys()
#         df['audienceId'] = self.dict.values()
        
#         csv_buffer = StringIO()
#         df.to_csv(csv_buffer,index = False)
#         S3Auth.s3r.Object(S3Auth.bucketName,S3Auth.bucketKey).put(Body=csv_buffer.getvalue())
        
        
        
        
        
# class S3Auth():
#     def __init__(self,s3r,s3c,bucketName, bucketKey):
#         self.s3r = s3r
#         self.s3c = s3c
#         self.bucketName = bucketName
#         self.bucketKey = bucketKey
        
        
            
            
        
        
        
        
        
    
# class FreewheelAdvertiser():
#     def __init__(self,Name,ID):
#         self.Name = Name
#         self.ID = ID
        
# class  FreewheelAdvertiserList():
#     def __init__(self,freewheel_auth):
    
#         fw = freewheel_auth
#         url = 'https://api.freewheel.tv/services/v3/advertisers?status=ACTIVE&page=1&per_page=50'
#         get = xmltodict.parse(rs.get(url,headers = fw.xml).text,dict_constructor = dict)

#         audience_list = []
#         numberOfPages = int(get['advertisers']['@total_pages'])
#         print(numberOfPages)

#         for i in range(numberOfPages):
#             try:
#                 url = f'https://api.freewheel.tv/services/v3/advertisers?status=ACTIVE&page={i+1}&per_page=50'
#                 get = xmltodict.parse(rs.get(url,headers = fw.xml).text,dict_constructor = dict)
#                 for item in get['advertisers']['advertiser']:
#                     FWA = FreewheelAdvertiser(Name = item['name'], ID = item['id'])
#                     audience_list.append(FWA)
#             except ConnectionError:
#                 continue

#         self.list = audience_list
        
        
    
# class FreewheelCampaign():
#     def __init__(self,Name,ID):
#         self.Name = Name
#         self.ID = ID
        
# class  FreewheelCampaignList():
#     def __init__(self,freewheel_auth):
    
#         fw = freewheel_auth
#         url = 'https://api.freewheel.tv/services/v3/campaigns?status=ACTIVE&page=1&per_page=50'
#         get = xmltodict.parse(rs.get(url,headers = fw.xml).text,dict_constructor = dict)

#         audience_list = []
#         numberOfPages = int(get['campaigns']['@total_pages'])
#         print(numberOfPages)

#         for i in range(numberOfPages):
#             url = f'https://api.freewheel.tv/services/v3/campaigns?status=ACTIVE&page={i+1}&per_page=50'
#             try:
#                 get = xmltodict.parse(rs.get(url,headers = fw.xml).text,dict_constructor = dict)
#                 for item in get['campaigns']['campaign']:
#                     FWA = FreewheelCampaign(Name = item['name'], ID = item['id'])
#                     audience_list.append(FWA)
#             except ConnectionError:
#                 continue 

#         self.list = audience_list
        
        
        
# class FreewheelIO():
#     def __init__(self,Name,ID):
#         self.Name=  Name
#         self.ID = ID
        
    

# def PushIO(freewheel_auth,FreewheelAdvertiser,FreewheelCampaign,name,status):
#     fw = freewheel_auth
#     adv = FreewheelAdvertiser
#     camp =FreewheelCampaign

#     url = f'https://api.freewheel.tv/services/v3/campaign/{camp.ID}/insertion_order'
#     data = {'insertion_order': {'name' : name, 'status' : status, 'advertiser_id' : adv.ID}}
#     io = xmltodict.parse(rs.post(url,headers=fw.xml,data=dict2xml(data)).text,dict_constructor = dict)

#     IO = FreewheelIO(Name = name, ID = io['insertion_order']['id'])

#     IO.status = status
#     IO.campaign = io['insertion_order']['campaign_id']

#     return IO


# def CopyPlacement(freewheel_auth,name,FreewheelIO,targetPID,targets):
#     fw = freewheel_auth
#     IO = FreewheelIO
#     get_url = f'https://api.freewheel.tv/services/v3/placements/{str(targetPID)}?show=all'
#     get = xmltodict.parse(rs.get(get_url,headers=fw.xml).text,dict_constructor = dict)
#     placement = {'placement': {'name': name,
#                               'insertion_order_id' : IO.ID}}
#     for ITEM in targets:
#         print(ITEM)

#         if ITEM == 'content_targeting':
#             content = get['placement'][ITEM]
#             if type(content['include']['set']) == dict:
#                 del content['include']['relation_between_sets']
#             if type(content['include']['remaining_items']) ==  type(None):
#                 del content['include']['remaining_items']

#             placement['placement']['content_targeting'] = content 

#         elif ITEM == 'ad_product':
#             adUnitList = []
#             ad_product = get['placement'][ITEM]
#             for item in ad_product['ad_unit_node']:
#                 nodeDict = {}
#                 for key in item.keys():
#                     if type(item[key]) == type(None):
#                         continue
#                     elif key != 'ad_unit_node_id':
#                         nodeDict[key] = item[key]

#                 adUnitList.append(nodeDict)
#             linkMethod = get['placement']['ad_product']['link_method']

#             placement['placement']['ad_product'] = {'link_method': linkMethod, 'ad_unit_node': adUnitList }
#         elif ITEM == 'budget':
#             copyBudget = get['placement']['budget']
#             if copyBudget['budget_model'] == 'IMPRESSION_TARGET':
#                 targetBudget = {}
#                 for item in copyBudget.keys():
#                     if type(None) == type(copyBudget[item]):
#                         continue
#                     else:
#                         targetBudget[item] = copyBudget[item]
            
#             placement['placement']['budget'] = targetBudget

            
#         elif ITEM == 'delivery':
#             copyDelivery = get['placement']['delivery']
#             targetDelivery = {}
#             for item in copyDelivery.keys():
#                 if type(None) == type(copyDelivery[item]):
#                     continue
#                 else:
#                     targetDelivery[item] = copyDelivery[item]
                    
#             placement['placement']['delivery'] = targetDelivery
            
        
#     createpid = rs.post('https://api.freewheel.tv/services/v3/placement/create',headers=fw.xml,data=dict2xml(placement))
#     pid = xmltodict.parse(createpid.text,dict_constructor=dict)['placement']['id']

#     copyPlacement =  Placement(fw,IO= IO ,attach= {'attach' : 'No'})
#     copyPlacement.Name = name
#     copyPlacement.PID = pid


#     if 'ad_product' in targets:
#         getCopyUrl = f'https://api.freewheel.tv/services/v3/placements/{copyPlacement.PID}?show=all'
#         getCopy = xmltodict.parse(rs.get(getCopyUrl,headers=fw.xml).text,dict_constructor = dict)
#         creativeMap = []

#         for au in getCopy['placement']['ad_product']['ad_unit_node']:

#             creativeMap.append({'node' : au['ad_unit_node_id'], 'unit': au['ad_unit_id'] , 'creative' : []})



#     copyPlacement.creativeMap = creativeMap
#     copyPlacement.Budget = targetBudget
#     copyPlacement.Delivery = targetDelivery

#     return copyPlacement



# class Placement():
#     def __init__(self,freewheel_auth,IO= None,attach= None):
#         try:
#             if attach['attach'] ==  'Yes':
#                 self.freewheel_auth = freewheel_auth
#                 headers = self.freewheel_auth.xml
#                 self.PID = attach['PID'] 
#                 node = 'all'
#                 get_url = f'https://api.freewheel.tv/services/v3/placements/{str(self.PID)}?show={node}'
#                 get_placement = rs.get(get_url,headers=headers).text
#                 self.dict = xmltodict.parse(get_placement,dict_constructor=dict)
#                 self.Name  = self.dict['placement']['name']
#             elif attach['attach'] == 'No':

#                 try:
#                     self.freewheel_auth = freewheel_auth
#                     self.IO = IO
#                 except:
#                     raise Exception("invalid username or password")
                
#         except:
#             raise Exception("invalid username or password")
            
            
#     def UpdateFlight(self,startDate,endDate):
#         time = {'time_zone': '(GMT-05:00) America - New York',
#  'start_time':startDate,
#  'end_time': endDate}

#         data = dict2xml({'placement':{'schedule' : time}})

#         put = rs.put(f'https://api.freewheel.tv/services/v3/placements/{self.PID}',headers=self.freewheel_auth.xml,data=data)
#         return xmltodict.parse(put.text,dict_constructor = dict)
                
#     def AttachCreatives(self):
#         putList = []
#         for item in self.creativeMap:
#             aun = item['node']
#             for cre in item['creative']:
#                 cput = rs.put(f'https://api.freewheel.tv/services/v3/ad_unit_nodes/{aun}/creatives/{cre}.xml',headers=fw.xml).text
#                 putList.append(xmltodict.parse(cput,dict_constructor = dict))

#         return putList
    
    
#     def includeDmaTargeting(self,list_of_codes):

#         headers = self.freewheel_auth.xml
#         geo_type = 'dma'
#         inc_exc  = 'include'
#         dict_obj = {}
#         dict_obj['geography_targeting'] = {inc_exc :{geo_type: list_of_codes }}
#         data = dict2xml({'placement' : dict_obj})
#         put = rs.put(f'https://api.freewheel.tv/services/v3/placements/{self.PID}',headers=headers,data=data).text
#         return xmltodict.parse(put,dict_constructor = dict)

#     def excludeDmaTargeting(self,list_of_codes):

#         headers = self.freewheel_auth.xml
#         geo_type = 'dma'
#         inc_exc  = 'exclude'
#         dict_obj = {}
#         dict_obj['geography_targeting'] = {inc_exc :{geo_type: list_of_codes }}
#         data = dict2xml({'placement' : dict_obj})
#         put = rs.put(f'https://api.freewheel.tv/services/v3/placements/{self.PID}',headers=headers,data=data).text
#         return xmltodict.parse(put,dict_constructor = dict)


#     def excludeStateTargeting(self,list_of_codes):

#         headers = self.freewheel_auth.xml
#         geo_type = 'state'
#         inc_exc  = 'exclude'
#         dict_obj = {}
#         dict_obj['geography_targeting'] = {inc_exc :{geo_type: list_of_codes }}
#         data = dict2xml({'placement' : dict_obj})
#         put = rs.put(f'https://api.freewheel.tv/services/v3/placements/{self.PID}',headers=headers,data=data).text
#         return xmltodict.parse(put,dict_constructor = dict)

#     def includeStateTargeting(self,list_of_codes):

#         headers = self.freewheel_auth.xml
#         geo_type = 'state'
#         inc_exc = 'include'
#         dict_obj = {}
#         dict_obj['geography_targeting'] = {inc_exc :{geo_type: list_of_codes }}
#         data = dict2xml({'placement' : dict_obj})
#         put = rs.put(f'https://api.freewheel.tv/services/v3/placements/{self.PID}',headers=headers,data=data).text
#         return xmltodict.parse(put,dict_constructor = dict)

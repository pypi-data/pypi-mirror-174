import json
from lib2to3.pgen2 import token
import requests

class api:
  def __init__(self,apikey,apisecret,broker,version="1.0"):
     self.apikey=apikey 
     self.apisecret=apisecret
     self.burl = "https://" + broker + 'api.algomojo.com/' + str(version) + '/'
  def place_order(self,exchange,ticker,action,ordertype,qty,product,variety__="NORMAL",price=0,discqty=0,trigprce=0,sqoff=0,stoploss=0,trailstoploss=0):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                       "stgy_name": "Test Strategy",
                       "variety":variety__,
                       "tradingsymbol":ticker,
                       "symboltoken":"",
                       "transactiontype":action,
                       "exchange":exchange,
                       "ordertype":ordertype,
                       "producttype":product,
                       "duration":"DAY",
                       "price":str(price),
                       "squareoff":str(sqoff),
                       "stoploss":str(stoploss),
                         "quantity":qty,
                       "triggerprice": str(trigprce),
                        "trailingStopLoss":str(trailstoploss),
                        "disclosedquantity":str(discqty),
                        "is_amo":"YES"
                      } 
           }
    url= self.burl + "PlaceOrder"   
    response = requests.post(url,json.dumps(data), headers={'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return jsonValue



 
  def place_multi_order(self, order_list):
    l =order_list
    for i in range(len(l)):
      l[i]["exchange"]=l[i]["exchange"]
      l[i]["tradingsymbol"]=str(l[i]["ticker"])
      l[i]["quantity"]=str(l[i]["qty"])
      l[i]["producttype"]=l[i]["product"]
      l[i]["price"]= str(l[i]["price"])
      l[i]["transactiontype"]=l[i]["action"]
      l[i]["ordertype"]=l[i]["ordertype"]
      l[i]["squareoff"]=l[i]["sqoff"]
      l[i]["stoploss"]=l[i]["stoploss"]
      l[i]["variety"]= "NORMAL" 
      l[i]["stgy_name"]="stgname"
      l[i]["duration"]="DAY"
      l[i]["symboltoken"]=l[i]["token"]
      l[i]["user_apikey"]=l[i]["user_apikey"]
      l[i]["api_secret"]=l[i]["api_secret"]
      l[i]["triggerprice"]=l[i]["trigprice"]
      l[i]["trailingStopLoss"]=l[i]["trailstoploss"]
      l[i]["order_refno"]="1"
      l[i]["disclosedquantity"]=l[i]["discqty"]
    
             
        
    data = {
              "api_key": self.apikey,
              "api_secret": self.apisecret,
              "data":
                {
                   "orders": l
                }
            }
    print(data)     
    url = self.burl + "PlaceMultiOrder"        
    response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return jsonValue          
                
    

      
      
     
  def place_option_order(self,spot,expiry,action,optiontype,ordertype,qty,strike,variety__="NORMAL",price=0,product='CARRYFORWARD ',trigprice="0",offset='1',stgname="options Strategy"):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
             "api_key":apikey,
             "api_secret":apisecret,
             "data":{ 
                         "stgy_name":"Options",
                         "variety":variety__,
                         "spot_sym":spot,
                         "expiry_dt":expiry,
                         "opt_type":optiontype,
                         "transactiontype":action,
                         "ordertype":ordertype,
                         "quantity":qty,
                         "price":str(price),
                         "triggerprice":str(trigprice),
                         "producttype":product,
                         "strike_int":strike,
                         "offset":offset 
                     
                    }
           }
    url = self.burl + "PlaceFOOptionsOrder"     
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue
  def modify_order(self,orderno,token,qty,ticker=0,exchange=0,product=0,ordertype=0,price=0):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                       "strg_name":"Test Strategy",
                       "variety":"NORMAL",
	                     "orderid":str(orderno),
		                   "ordertype":str(ordertype),
		                   "producttype":str(product),
		                   "duration":"DAY",
		                   "price":str(price),
	                     "quantity":str(qty),
		                   "tradingsymbol":str(ticker),
		                   "symboltoken":str(token),
		                   "exchange":str(exchange)
                  }
             }
    url = self.burl + "ModifyOrder"           
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue         

  def cancel_order(self,orderno):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                    "variety":"NORMAL",
		                "orderid":orderno,
                   }
             }
    url = self.burl +"CancelOrder"          
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue        
              
  def Profile(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            
             }
    url = self.burl +"Profile"          
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue                  

  def Limits(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
           
             }
    url = self.burl +"Limits"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue 

  def holdings(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
           
             }
    url = self.burl +"Holdings"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue  

  def order_book(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
           
             }
    url = self.burl +"OrderBook"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue       

  def positions(self,orderno):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            }
    url = self.burl +"Positions"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue  

  def trade_book(self):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
         
             }
    url = self.burl +"TradeBook"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue             
                              
 
  def feed(self,exchange,trading_symbol,token_symbol):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data": {
                     "exchange":exchange,
		                  "tradingsymbol":trading_symbol,
		                  "symboltoken":token_symbol,
                    } 
            }
    url = self.burl +"Feed"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue                                         

  def fetchtoken(self,tokenfetch):
    apikey=self.apikey
    apisecret=self.apisecret
    data = {
            "api_key":apikey,
            "api_secret":apisecret,
            "data":{
                     "s":tokenfetch
                    }
             }
    url = self.burl +"fetchtoken"         
    response = requests.post(url,json.dumps(data), headers= {'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue 


  









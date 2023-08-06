
Metadata-Version: 2.1

Name: algomojo-angel

Version: 0.92

Summary: A functional python wrapper for  trading api

Home-page: 

Author: Algomojo

Author-email: support@algomojo.com

License: MIT

Description: 
        ## ABOUT
        A functional python wrapper for firststock trading api.
        It is a python library for the [Algomojo Free API + Free Algo Trading Platform ](https://algomojo.com/). 
        It allows rapid trading algo development easily, with support for both REST-API interfaces. 
        Execute Orders in Reatime, Modify/Cancel Orders, Retrieve Orderbook, Tradebook, Open Positions, Squareoff Positions and much more functionalities. 
        For more details of each API behavior, Pease see the Algomojo API documentation.
        
        
        ## License
        
         Licensed under the MIT License.

        
        ## Documentation
        [Algomojo Rest API documentation ](https://algomojo.com/docs/python)
        
        
        
        
        ## Installation
        Install from PyPI
        
        	pip install algomojo-angel
        
        Alternatively, install from source. Execute setup.py from the root directory.
        python setup.py install
        
        Always use the newest version while the project is still in alpha!
        
        
        ## Usage Examples
        In order to call Algomojo trade API, you need to sign up for an trading account with one of the partner broker and obtain API key pairs and enjoy unlimited access to the API based trading.
         Replace api_key and api_secret_key with what you get from the web console.
        
        
        
        
        ## Getting Started
        
        After downloading package import the package and create the object with api credentials
        
        
        	from algomojo import angel
        
        
        
        
        
        ## Creating  Object
        
        For creating an object there are 3 arguments which would be passed
        
                 api_key : str
                     User Api key (logon to algomojo account to find api credentials)
                 api_secret : str
                     User Api secret (logon to algomojo account to find api credentials)
                 Broker : str
                     This takes broker it generally consists 2 letters , EX: angel--> an,
        
        Sample:
        	
        	at=angel.api(api_key="20323f062bb71ca6fbb178b4df8ac5z6",
        		    api_secret="686786a302d7364d81badc233f1d22e3",
        		    broker="an")
        
        
        
        
        
        
        ## Using Object Methods
        obj.method(mandatory_parameters)  or obj.method(madatory_parameters+required_parameters)
        
        
        # Avaliable Methods
        	
        ### 1. place_order:  
        
        		Function with mandatory parmeters: 
        				place_order(exchange,ticker,action,ordertype,qty,product)
        		
        		Function with all parametrs:       
        				place_order(exchange,ticker,action,ordertype,qty,product,price,
						dscqty,trigprc,sqoff,stoploss,trailstoploss)
                 	 
                        Sample :        
        				X=at.place_order(exchange="NSE",ticker="SBIN-EQ",action="BUY",
						ordertype="MARKET",qty="12",product="DELIVERY")
        
        		place_multi_order(order_list)

	            Sample order_list: 
	             [{"user_apikey":"xxxxxxxxxxxxxxxxxxxxxxxxx",
	             "api_secret":"xxxxxxxxxxxxxxxxxxxxx","ticker":"INFY-EQ",
	             "exchange":"NSE","action":"BUY","qty":"1","price":"500","ordertype":"MARKET",
	             "product":"DELIVERY","trigprice":"0","discqty":"0","stoploss":"0","sqoff":"0",
                 "trailstoploss":"0","token":"1594"},
		           {"user_apikey":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
		             "api_secret":"xxxxxxxxxxxxxxxxxxxxxxxx","ticker":"INFY-EQ",
		             "exchange":"NSE","action":"BUY","qty":"10","price":"200","ordertype":"MARKET",
		             "product":"DELIVERY","trigprice":"0","discqty":"0","stoploss":"0","sqoff":"0",
		             "trailstoploss":"0","token":"1594"}]	

	         Sample function call:  
		         at.place_multi_order(order_list)
        
        ### 3. place_option_order
        
        		Funtion with mandatory parameters:  
        			     place_option_order(spot,expiry,action,optiontype,ordertype,qty,strike)
        		Function with all parameters: 
        		 
        		            place_option_order(spot,expiry,action,optiontype,ordertype,qty,strike,
							price,product,trigprice,offset,variety__)
        		
        		Sample :          
        		       Z=at.place_option_order(spot="NIFTY",expiry="07APR22",action="BUY",optiontype="CE",
						ordertype="MARKET",qty="50",strike="100",product="CARRYFORWARD")
        		
        ### 4. modify_order:
        
        		Funtion with mandatory parameters:  
        			     	modify_order(orderno,token,qty)
        		
        		Function with all parameters:
        		 	      	modify_order(orderno,exchange,ticker,ordertype,qty,prc,trigprice)
        		
        		Sample : `		   
        				at.modify_order("220401000439413","1594","3")
        		
        		
        		
        
        
        
        ### 5. cancel_order
        
        		Funtion with mandatory parameters:   
        				cancel_order(orderno)
        
        		Function with all parameters:          
        		
        				cancel_order(orderno)
        
        		Sample:             
        				at.cancel_order(orderno="4567891523")

        
        		
        
        ### 6. profile:
        
        		Funtion with mandatory parameters:   
        					profile()
        					
        		Function with all parameters:        
        					profile()
        					
        		Sample:                              
        					at.profile()
        					             
        
        ### 7. limits
        
        
        		Funtion with mandatory parameters:   
        					limits()
        					
        		Function with all parameters:        
        					limits()
        					
        	        Sample:                              
        					at.limits()
        		                                    
        
        
        
        
        
        ### 8. holdings: 
        
        		Funtion with mandatory parameters:   
        					holdings()
        					
        		Function with all parameters:       
        					holdings()
        					
        		Sample:                              
        					at.holdings()
        
        
        
        ### 9. order_book:
        
        
        		Funtion with mandatory parameters:   
        					order_book()
        		
        		Function with all parameters:        
        					order_book()
        					
        		Sample:                             
        					at.order_book()
        
        
        
        
        
        ### 10. positions
        
        
        		Funtion with mandatory parameters:   
        					positions(orderno))
        					
        		Function with all parameters:        
        					positions(orderno))
        					
        		Sample:                              
        					at.positions(orderno='201109000000025')
        
        
        
        
        ### 11. trade_book
                
             	Funtion with mandatory parameters:   
        					trade_book()
        					
        		Function with all parameters:        
        					trade_book()
        					
        		Sample:                              
        					at.trade_book()
        
                    
        					
        
        		
        		
        		
        
        
        
        
        ### 12. feed
                
             	Funtion with mandatory parameters:   
        					feed(exchange,trading_symbol,token_symbol)
        					
        		Function with all parameters:        
        					feed(exchange,trading_symbol,token_symbol)
        					
        		Sample:                              
        					at.feed()
        
        
        
        ### 13.  fetchtoken
                
             	Funtion with mandatory parameters:   
        					fetchtoken(tokenfetch)
        					
        		Function with all parameters:        
        					fetchtoken(tokenfetch)
        					
        		Sample:                              
        					at.fetchtoken(tokenfetch="2645")
        
       
    
         
        
        
        
        
        
Platform: UNKNOWN
Classifier: License :: OSI Approved :: MIT License
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 2
Classifier: Programming Language :: Python :: 3
Description-Content-Type: text/markdown

import requests

heador  ={"q":"help","JSESSIONID":"12345678"}
s = requests.Session()
r =s.get("https://console.dialogflow.com/api-client/demo/embedded/ae8f0bd9-70e2-47c8-b30c-7e57e41ad17" ,verify = False)
#rresponse  = r.json()
#print(r.text)
cookies = r.cookies.get_dict()
sessionid  =  cookies['JSESSIONID']
print(sessionid)
r = s.get("https://console.dialogflow.com/api-client/demo/embedded/ae8f0bd9-70e2-47c8-b30c-7e57e41ad170/demoQuery?q=help me&sessionId="+sessionid)
rresponse  = r.json()
cookies = r.cookies.get_dict()

print(rresponse)
print(cookies)
r = s.get("https://console.dialogflow.com/api-client/demo/embedded/ae8f0bd9-70e2-47c8-b30c-7e57e41ad170/demoQuery?q=help me with telephony&sessionId="+sessionid)
rresponse  = r.json()
cookies = r.cookies.get_dict()
print(rresponse)
print(cookies)
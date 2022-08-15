import requests
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
import os 
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
#/////////////////////////////////////////////SETTING UP THINGS //////////////////////////////////////////////////////////
load_dotenv()
TEQUILLA_API=os.getenv("TEQUILLA_API")                      # THIS WILL BE CREATED WHEN YOU CREATE AN ACCOUNT ON TEQUILLA AND CREATE A SOLUTION
ACC_SSID=os.getenv("ACC_SSID")                              #THIS IS THE TWILIO SSID
AUTH_TOKEN=os.getenv("AUTH_TOKEN")                           #THIS IS THE  AUTH TOKEN OF TWILIO
MY_NUMBER=os.getenv("MY_NUMBER")                             #THIS IS THE YOU GET FROM THE TWILIO  ACCOUNT  
P_NUM=os.getenv("P_NUM")                                     #THIS IS  THE TO WHICH YOU WANNA SEND THE SMS
TEQUILLA_ENPOINT=os.getenv("TEQUILLA_ENPOINT")               #THIS ENPOINT YOU CAN GET FROM WEBSITE 
SHEET_ID=os.getenv("SHEET_I2")                                 #ID OF THE GOOGLE SHEET WHERE YOU HAVE INSERTED THE DATA
SERVICE_ACCOUNT_FILE = 'keys.json'                              # THIS FILE CONTAINS THE CREDENTIALS OF THE GOOGLE SHEETS API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds=None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
#///////////////////////////////////////LOADING DATA FROM THE SHEET TO THE LIST TO SEARCH ONE BY ONE////////////////////////////////////////////////////////////////
Iata_Codes=sheet.values().get(spreadsheetId=SHEET_ID,range='data!B2:B10').execute().get('values')
Min_price=sheet.values().get(spreadsheetId=SHEET_ID,range='data!C2:C10').execute().get('values')
Cities=sheet.values().get(spreadsheetId=SHEET_ID,range='data!A2:A10').execute().get('values')
for x in range(len(Iata_Codes)):
    Iata_Codes[x]=str(Iata_Codes[x]).join(map(str,Iata_Codes[x]))
    Min_price[x]=str(Min_price[x]).join(map(str,Min_price[x]))
    Cities[x]=str(Cities[x]).join(map(str,Cities[x]))
#///////////////////////////////////////////SETTING THE PARAMS BY LOOPING IN THE LIST CREATED FROM THE SHEEET////////////////////////////////////////////////////////////

header={
    'apikey':TEQUILLA_API
}
Prices=[]
count=0
for x in range(len(Iata_Codes)):
    print("Running for city "+ str(count))
    count+=1
    parameters={
        'fly_from':'LON',
        'fly_to':Iata_Codes[x],
        'date_from':'15/09/2022',
        'date_to':'15/12/2022',
        'selected_cabins':'M',
        'curr':'GBP',
        'price_to': Min_price[x]
    }

    response=requests.get(url=TEQUILLA_ENPOINT,params=parameters,headers=header)

    try:
        Price=str(response.json()['data'][0]['price'])
        Prices.append(Price)
        Message="PACK YOUR BAGS!!🥳 \nLET'S GO TO " + Cities[x]+"\n" + "IT'S A PRICE DROP @£" + str(Prices[x])+" " + str(parameters['date_from']) +'to ' + str(parameters['date_to'])
        proxy_client=TwilioHttpClient()
        client=Client(ACC_SSID,AUTH_TOKEN)
        message=client.messages \
            .create(
                body = Message,
                from_= MY_NUMBER,
                to = P_NUM
            )
        print(message.sid)
        print(Message)
    except:
        Price="NA"           #This will not get sms to you since price will not be lower than your minimum price!
        Prices.append(Price)
    
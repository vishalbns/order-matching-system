import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle
import main_trigger

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# here enter the id of your google sheet
SAMPLE_SPREADSHEET_ID_input = '1WYScLRCDOXL1zZK6nma6InmkDDvjrOAN4I8gVo2I7uM'
SAMPLE_RANGE_NAME = 'A1:AA1000'

def main():
    global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/vishalbns/Desktop/angular-flask/credentials.json', SCOPES) # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                range=SAMPLE_RANGE_NAME).execute()
    values_input = result_input.get('values', [])

    if not values_input and not values_expansion:
        print('No data found.')

main()

df=pd.DataFrame(values_input[1:], columns=values_input[0])
print(df)

#change this by your sheet ID
SAMPLE_SPREADSHEET_ID_input = '1WYScLRCDOXL1zZK6nma6InmkDDvjrOAN4I8gVo2I7uM'

#change the range if needed
SAMPLE_RANGE_NAME = 'A2:C2'

def Create_Service(client_secret_file, api_service_name, api_version, *scopes):
    global service
    SCOPES = [scope for scope in scopes[0]]
    #print(SCOPES)
    
    cred = None

    if os.path.exists('token_write.pickle'):
        with open('token_write.pickle', 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            cred = flow.run_local_server()

        with open('token_write.pickle', 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(api_service_name, api_version, credentials=cred)
        print(api_service_name, 'service created successfully')
        #return service
    except Exception as e:
        print(e)
        #return None
        
# change 'my_json_file.json' by your downloaded JSON file.
Create_Service('/Users/vishalbns/Desktop/angular-flask/credentials.json', 'sheets', 'v4',['https://www.googleapis.com/auth/spreadsheets'])


def Export_Data_To_Sheets(orderList, number_of_user_orders):
    newOrdersSheetData = service.spreadsheets().values().get(
        spreadsheetId='1WYScLRCDOXL1zZK6nma6InmkDDvjrOAN4I8gVo2I7uM',
        range='NewOrders!A1:AA1000'
    ).execute()
    #print(newOrdersSheetData['values'])
    newRowIndex = len(newOrdersSheetData['values'])
    #print(newRowIndex)
    orderList.insert(0, 29+newRowIndex)
    response_date = service.spreadsheets().values().update(
        spreadsheetId='1WYScLRCDOXL1zZK6nma6InmkDDvjrOAN4I8gVo2I7uM',
        valueInputOption='RAW',
        range='NewOrders!A' + str(newRowIndex+1) + ':F' + str(newRowIndex+1),
        body=dict(
            majorDimension='ROWS',
            values=[orderList])
    ).execute()
    if(newRowIndex <= number_of_user_orders):
        #main_trigger.main_trigger(30,number_of_user_orders,orderList)
        main_trigger.input_user_order(number_of_user_orders, orderList)
    print('Sheet successfully Updated')

def Export_ExecutedTrades_To_Sheets(executedTrades):
    for i in range(0,len(executedTrades)):
        response_data = service.spreadsheets().values().update(
            spreadsheetId='1WYScLRCDOXL1zZK6nma6InmkDDvjrOAN4I8gVo2I7uM',
            valueInputOption='RAW',
            range='TradeBook!A' + str(i+2) + ':E' + str(i+2),
            body=dict(
                majorDimension='ROWS',
                values=[executedTrades[i]])
        ).execute()

def Export_CancelledTrades_To_Sheets(cancelledTrades):
    for i in range(0,len(cancelledTrades)):
        response_data = service.spreadsheets().values().update(
            spreadsheetId='1WYScLRCDOXL1zZK6nma6InmkDDvjrOAN4I8gVo2I7uM',
            valueInputOption='RAW',
            range='CancelledOrders!A' + str(i+2) + ':E' + str(i+2),
            body=dict(
                majorDimension='ROWS',
                values=[cancelledTrades[i]])
        ).execute()
    
def clear_g_sheets():
    response_cleartradebook = service.spreadsheets().values().clear(
        spreadsheetId='1WYScLRCDOXL1zZK6nma6InmkDDvjrOAN4I8gVo2I7uM',
        range = 'TradeBook!A2:E40'
    ).execute()
    response_clearcancelsheet = service.spreadsheets().values().clear(
        spreadsheetId='1WYScLRCDOXL1zZK6nma6InmkDDvjrOAN4I8gVo2I7uM',
        range =  'CancelledOrders!A2:E40'
    ).execute()
    response_clearnewordersheet = service.spreadsheets().values().clear(
        spreadsheetId='1WYScLRCDOXL1zZK6nma6InmkDDvjrOAN4I8gVo2I7uM',
        range =  'NewOrders!A2:F10'
    ).execute()
    response_clearallordersheet = service.spreadsheets().values().clear(
        spreadsheetId='1WYScLRCDOXL1zZK6nma6InmkDDvjrOAN4I8gVo2I7uM',
        range =  'AllOrders!A2:F40'
    ).execute()

def Export_AllOrders_To_Sheets(AllOrders):
    print(AllOrders)
    for i in range(0,len(AllOrders)):
        response_data = service.spreadsheets().values().update(
            spreadsheetId='1WYScLRCDOXL1zZK6nma6InmkDDvjrOAN4I8gVo2I7uM',
            valueInputOption='RAW',
            range='AllOrders!A' + str(i+2) + ':F' + str(i+2),
            body=dict(
                majorDimension='ROWS',
                values=[AllOrders[i]])
        ).execute()
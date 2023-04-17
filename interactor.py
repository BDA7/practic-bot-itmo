import os

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

# id таблицы https://docs.google.com/spreadsheets/d/xxxxx/edit#gid=0
sheetId = "1LudWwZpHk3wrqkZkX103py7NVM7oUA6Yctjrnog63UA"


# Загрузка данных в гугл таблицу
async def loadDataToSheet(data):
    creds_json = os.path.dirname(__file__) + "/practice-384008-81be211bdbe4.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())

    service = build('sheets', 'v4', http=creds_service)
    sheet = service.spreadsheets()
    body = {
        'values': [
            [data['name'], data['group'], data['educational_practice'], data['educational_practice_2'],
             data['industrial_practice'], data['other_industrial_practice'], data['work_industrial_practice'],
             data['other_industrial_practice_fileName'], data['undergraduate_practice']]
        ]
    }

    sheet.values().append(
        spreadsheetId=sheetId,
        range="Лист1!A1",
        valueInputOption="RAW",
        body=body
    ).execute()
    resp = sheet.values().batchGet(spreadsheetId=sheetId, ranges=["Лист1"]).execute()


# Получение популярных вопросов с таблицы
async def getQuestions():
    creds_json = os.path.dirname(__file__) + "/practice-384008-81be211bdbe4.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())

    service = build('sheets', 'v4', http=creds_service)
    sheet = service.spreadsheets()
    resp = sheet.values().batchGet(spreadsheetId=sheetId, ranges=["Лист2"]).execute()
    questions = resp['valueRanges'][0]['values']
    return questions

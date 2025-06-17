import gspread
from google.oauth2.service_account import Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("server/credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1aS_RncSOZyQ2PjkBUbK2wP3NuweIIooTjVOnxhCtmzk"
workbook = client.open_by_key(sheet_id)

def rename_sheet_from_cell():
    sheet_to_rename = workbook.worksheet("en cours")



    print(sheet_to_rename.id)
    #sheet_id = sheet_to_rename['properties']['sheetId']


    date = sheet_to_rename.get_values('A2')[0][0]
    print(date)


rename_sheet_from_cell()

#def rename_sheet_from_cell(service, spreadsheet_id):
#    try:
#        # 1. Lire les métadonnées du document pour récupérer les sheets existantes
#
#        sheets = spreadsheet.get('sheets', [])
#
#        # 2. Trouver la feuille appelée "en cours"
#        sheet_to_rename = next((s for s in sheets if s['properties']['title'] == 'en cours'), None)
#        if not sheet_to_rename:
#            print("❌ Feuille 'en cours' introuvable.")
#            return False
#
#        sheet_id = sheet_to_rename['properties']['sheetId']
#
#        # 3. Lire la cellule A2 de la feuille "en cours"
#        result = service.spreadsheets().values().get(
#            spreadsheetId=spreadsheet_id,
#            range="'en cours'!A2"
#        ).execute()
#
#        new_title = result.get('values', [[None]])[0][0]
#        if not new_title:
#            print("❌ La cellule A2 est vide.")
#            return False
#
#        # 4. Construire la requête de renommage
#        requests = [{
#            'updateSheetProperties': {
#                'properties': {
#                    'sheetId': sheet_id,
#                    'title': new_title
#                },
#                'fields': 'title'
#            }
#        }]
#
#        # 5. Envoyer la requête via batchUpdate
#        body = {'requests': requests}
#        response = service.spreadsheets().batchUpdate(
#            spreadsheetId=spreadsheet_id,
#            body=body
#        ).execute()
#
#        print(f"✅ Feuille renommée en '{new_title}' avec succès.")
#        return True
#
#    except HttpError as err:
#        print(f"Erreur API : {err}")
#        return False
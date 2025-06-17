import gspread
from google.oauth2.service_account import Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1aS_RncSOZyQ2PjkBUbK2wP3NuweIIooTjVOnxhCtmzk"
workbook = client.open_by_key(sheet_id)

current_sheet = workbook.sheet1

row_values = current_sheet.row_values(1)
print (row_values)

row_values=["8/12/20025", 930, 29, 99]
current_sheet.append_row(row_values, value_input_option='USER_ENTERED')

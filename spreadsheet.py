import os
import json
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class EditSpreadSheet():
  def __init__(self):
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    path += '/rn-1-a615ac4d9dff.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
    global gc
    gc = gspread.authorize(credentials)
    worksheet = gc.open('info').sheet1

    self.worksheet = worksheet
  
  def detect_user_location(self, user_id):
    row = 1
    while self.worksheet.cell(row, 1).value != user_id:
      row += 1
    return self.worksheet.cell(row, 2).value

  def detect_last_row(self):
    row = 1
    while self.worksheet.cell(row, 1) != "":
      row += 1
    return row 

  def add_user_id(self, user_id):
    self.worksheet.update_cell(self.detect_last_row(), 1, user_id)
  
  def add_user_location(self, user_id, location):
    row = 1
    while self.worksheet.cell(row, 1).value != user_id:
      row += 1
    self.worksheet.update_cell(self.detect_last_row, 2, location)

  


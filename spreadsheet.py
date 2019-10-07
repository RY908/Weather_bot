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
    self.worksheet_list = worksheet.get_all_values()
    self.length = len(self.worksheet_list)
  
  def detect_user_location(self, user_id):
    for i in range(self.length):
      if self.worksheet_list[i][0] == user_id:
        return self.worksheet_list[i][1]

  def detect_last_row(self):
    for i in range(self.length):
      if self.worksheet_list[i][0] == "":
        return i+1
    return self.length

  def add_user_id(self, user_id):
    self.worksheet.update_cell(self.detect_last_row(), 1, user_id)
    return
  
  def add_user_location(self, user_id, location):
    for i in range(self.length):
      if self.worksheet_list[i][0] == user_id:
        self.worksheet.update_cell(i+1, 2, location)
    return
    #self.worksheet.update_cell(self.detect_last_row, 2, location)

  


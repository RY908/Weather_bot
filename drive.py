from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def uploadVideo(video):
  gauth = GoogleAuth()
  gauth.LocalWebserverAuth()

  drive = GoogleDrive(gauth)
  """
  f = drive.CreateFile({'title': 'TEST.txt'})
  f.SetContentString('Hello')
  f.Upload()
  """
  f = drive.CreateFile()
  f.SetContentFile(video)
  #f.SetContentFile("test.mp4")
  f.Upload()

def rename(user_id, name):
  gauth = GoogleAuth()
  gauth.LocalWebserverAuth()

  drive = GoogleDrive(gauth)
  file_id = drive.ListFile({'q': 'title = "{}.mp4"'.format(user_id)}).GetList()[0]['id']
  #"{}.mp4".format(user_id)
  f = drive.CreateFile({'id': file_id})
  f.FetchMetadata()
  f['title'] = '{}.mp4'.format(name)
  f['userPermission']['role'] ='anyone'
  f.Upload()
  permission = f.InsertPermission({
                        'type': 'anyone',
                        'value': 'anyone',
                        'role': 'reader'})
  #print(type(f))
  # <class 'pydrive.files.GoogleDriveFile'>
  #pprint.pprint(f)
  # GoogleDriveFile({'id': '1urYj2HbvV6kNfYsT8A-2PsmEjdiR2nZS'})

  f.FetchMetadata()

import pprint

def download(name):
  gauth = GoogleAuth()
  gauth.LocalWebserverAuth()

  drive = GoogleDrive(gauth)
  file_id = drive.ListFile({'q': 'title = "{}.mp4"'.format(name)}).GetList()[0]['id']
  f = drive.CreateFile({'id': file_id})
  f.FetchMetadata()
  #pprint.pprint(f)
  #f.GetContentFile('20191105あ.mp4')
  #print(f['downloadUrl'])
  #print(f['alternateLink'])
  link = f['alternateLink']
  return link

#rename("20191105あ", "20191105あ")
#print(download("20191105あ"))




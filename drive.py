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
  f.Upload()
  #print(type(f))
  # <class 'pydrive.files.GoogleDriveFile'>

  #print(f)
  # GoogleDriveFile({'id': '1urYj2HbvV6kNfYsT8A-2PsmEjdiR2nZS'})

  f.FetchMetadata()

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


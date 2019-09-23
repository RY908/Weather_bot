import requests
from bs4 import BeautifulSoup

url = "https://tenki.jp/"

r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')


def get_weather(word):
  content = soup.find_all(class_='forecast-map-entry')
  prefecture_list = []
  for pre in content:
    prefecture_list += [pre.get_text(' ').split()[0]]
    if word in pre:
      li = pre.get_text(' ').split()
      #print(li)
      #print(pre)
      weather = pre.find('img')
      #print(weather['src'])
      #print(weather['alt'])
      li.insert(1, weather['alt'])
      result = ("{}の今日の天気は{}、気温は{}/{}度、降水確率は{}です。".format(li[0], li[1], li[2], li[4], li[5]))
      return result
  #print(prefecture_list)
  result = '\n'.join(prefecture_list), '\n', 'の中から選択してください。'
  return result
    
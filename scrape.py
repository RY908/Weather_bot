import requests
from bs4 import BeautifulSoup

#url = "https://tenki.jp/"

#r = requests.get(url)
#soup = BeautifulSoup(r.text, 'lxml')


def get_weather(word):
  url = "https://tenki.jp/"
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  content = soup.find_all(class_='forecast-map-entry')
  prefecture_list = []
  for pre in content:
    prefecture_list += [pre.get_text(' ').split()[0]]
    if word in pre:
      li = pre.get_text(' ').split()
      weather = pre.find('img')
      li.insert(1, weather['alt'])
      result = ("{}の今日の天気は{}\n最高気温は{}度\n最低気温は{}度\n降水確率は{}です。".format(li[0], li[1], li[2], li[4], li[5]))
      return result
  result = ('\n'.join(prefecture_list)+'\n'+'の中から選択してください。')
  return result

def get_weather_from_location(location):
  print(location)
  url = "https://weather.yahoo.co.jp/weather/search/?p=" + location
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  content = soup.find(class_="serch-table")
  location_url = content.find('a')
  location_url = "http:" + location_url.get('href')
  r = requests.get(location_url)
  soup = BeautifulSoup(r.text, 'html.parser')
  content = soup.find(id='yjw_pinpoint_today')
  content = content.find_all('td')
  info = []

  for each in content[1:]:
    info.append(each.get_text().strip('\n'))
  
  time = info[:8]
  weather = info[9:17]
  temperature = info[18:26]
  weather_info = [(time[i], weather[i], temperature[i]) for i in range(8)]
  result = [('{0[0]}: {0[1]}, {0[2]}°C'.format(weather_info[i])) for i in range(8)]
  result = ('{}の今日の天気は\n'.format(location) + '\n'.join(result))

  return result


#print(get_weather_from_location('京都府'))
    